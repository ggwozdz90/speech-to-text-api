import multiprocessing
import multiprocessing.connection
import multiprocessing.synchronize
from dataclasses import dataclass
from multiprocessing.sharedctypes import Synchronized
from typing import Any, Tuple

import whisper

from data.workers.base_worker import BaseWorker


@dataclass
class WhisperConfig:
    device: str
    model_type: str
    model_download_path: str


class WhisperWorker(
    BaseWorker[  # type: ignore
        Tuple[str, str],
        dict[str, str],
        WhisperConfig,
        whisper.Whisper,
    ]
):
    def transcribe(
        self,
        file_path: str,
        language: str,
    ) -> dict[str, str]:
        if not self.is_alive():
            raise RuntimeError("Worker process is not running")

        self._pipe_parent.send(("transcribe", (file_path, language)))
        result = self._pipe_parent.recv()

        if isinstance(result, Exception):
            raise result

        return dict[str, str](result)

    def initialize_shared_object(
        self,
        config: WhisperConfig,
    ) -> whisper.Whisper:
        return whisper.load_model(
            config.model_type,
            download_root=config.model_download_path,
        ).to(config.device)

    def handle_command(
        self,
        command: str,
        args: Tuple[str, str],
        model: whisper.Whisper,
        config: WhisperConfig,
        pipe: multiprocessing.connection.Connection,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        if command == "transcribe":
            try:
                with processing_lock:
                    is_processing.value = True

                file_path, language = args
                kwargs: dict[str, Any] = {"language": language[:2]}

                if config.device == "cpu":
                    kwargs["fp16"] = False

                result = model.transcribe(file_path, **kwargs)
                pipe.send(result)

            except Exception as e:
                pipe.send(e)

            finally:
                with processing_lock:
                    is_processing.value = False
