import multiprocessing
import multiprocessing.connection
import multiprocessing.synchronize
from dataclasses import dataclass
from multiprocessing.sharedctypes import Synchronized
from typing import Any, Dict, Tuple

import whisper

from data.workers.base_worker import BaseWorker
from domain.exceptions.worker_not_running_error import WorkerNotRunningError


@dataclass
class WhisperSpeechToTextConfig:
    device: str
    model_type: str
    model_download_path: str
    log_level: str


class WhisperSpeechToTextWorker(
    BaseWorker[  # type: ignore
        Tuple[str, str, Dict[str, Any]],
        dict[str, str],
        WhisperSpeechToTextConfig,
        whisper.Whisper,
    ],
):
    def transcribe(
        self,
        file_path: str,
        language: str,
        transcription_parameters: Dict[str, Any],
    ) -> dict[str, str]:
        if not self.is_alive():
            raise WorkerNotRunningError()

        self._pipe_parent.send(
            (
                "transcribe",
                (
                    file_path,
                    language,
                    transcription_parameters,
                ),
            ),
        )
        result = self._pipe_parent.recv()

        if isinstance(result, Exception):
            raise result

        return dict[str, str](result)

    def initialize_shared_object(
        self,
        config: WhisperSpeechToTextConfig,
    ) -> whisper.Whisper:
        return whisper.load_model(
            config.model_type,
            download_root=config.model_download_path,
        ).to(config.device)

    def handle_command(
        self,
        command: str,
        args: Tuple[str, str, Dict[str, Any]],
        model: whisper.Whisper,
        config: WhisperSpeechToTextConfig,
        pipe: multiprocessing.connection.Connection,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        if command == "transcribe":
            try:
                with processing_lock:
                    is_processing.value = True

                file_path, language, transcription_parameters = args

                if "language" not in transcription_parameters:
                    transcription_parameters["language"] = language

                if "fp16" not in transcription_parameters:
                    transcription_parameters["fp16"] = config.device != "cpu"

                result = model.transcribe(file_path, **transcription_parameters)
                pipe.send(result)

            except Exception as e:
                pipe.send(e)

            finally:
                with processing_lock:
                    is_processing.value = False

    def get_worker_name(self) -> str:
        return type(self).__name__
