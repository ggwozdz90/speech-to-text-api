import multiprocessing
import multiprocessing.connection
import multiprocessing.synchronize
from dataclasses import dataclass
from multiprocessing.sharedctypes import Synchronized
from typing import Any, Dict, Tuple

from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText

from data.workers.base_worker import BaseWorker
from domain.exceptions.worker_not_running_error import WorkerNotRunningError


@dataclass
class SeamlessTranslationConfig:
    device: str
    model_name: str
    model_download_path: str
    log_level: str


class SeamlessTranslationWorker(
    BaseWorker[  # type: ignore
        Tuple[str, str, str, Dict[str, Any]],
        str,
        SeamlessTranslationConfig,
        Tuple[SeamlessM4Tv2ForTextToText, AutoProcessor],
    ],
):
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        translation_parameters: Dict[str, Any],
    ) -> str:
        if not self.is_alive():
            raise WorkerNotRunningError()

        self._pipe_parent.send(
            (
                "translate",
                (
                    text,
                    source_language,
                    target_language,
                    translation_parameters,
                ),
            ),
        )
        result = self._pipe_parent.recv()

        if isinstance(result, Exception):
            raise result

        return str(result)

    def initialize_shared_object(
        self,
        config: SeamlessTranslationConfig,
    ) -> Tuple[SeamlessM4Tv2ForTextToText, AutoProcessor]:
        model = SeamlessM4Tv2ForTextToText.from_pretrained(
            config.model_name,
            cache_dir=config.model_download_path,
        ).to(config.device)
        processor = AutoProcessor.from_pretrained(
            config.model_name,
            cache_dir=config.model_download_path,
        )
        return model, processor

    def handle_command(
        self,
        command: str,
        args: Tuple[str, str, str, Dict[str, Any]],
        shared_object: Tuple[SeamlessM4Tv2ForTextToText, AutoProcessor],
        config: SeamlessTranslationConfig,
        pipe: multiprocessing.connection.Connection,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        if command == "translate":
            try:
                with processing_lock:
                    is_processing.value = True

                text, source_language, target_language, translation_parameters = args
                model, processor = shared_object

                input_tokens = processor(
                    text,
                    src_lang=source_language,
                    return_tensors="pt",
                    padding=True,
                ).to(config.device)

                output_tokens = model.generate(
                    **input_tokens,
                    tgt_lang=target_language,
                    **translation_parameters,
                )[0].tolist()

                text_output = processor.decode(
                    output_tokens,
                    skip_special_tokens=True,
                )

                pipe.send("".join(text_output))

            except Exception as e:
                pipe.send(e)

            finally:
                with processing_lock:
                    is_processing.value = False

    def get_worker_name(self) -> str:
        return type(self).__name__
