import multiprocessing
import multiprocessing.connection
import multiprocessing.synchronize
from dataclasses import dataclass
from multiprocessing.sharedctypes import Synchronized
from typing import Any, Dict, Tuple

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from data.workers.base_worker import BaseWorker
from domain.exceptions.worker_not_running_error import WorkerNotRunningError


@dataclass
class MBartTranslationConfig:
    device: str
    model_name: str
    model_download_path: str
    log_level: str


class MBartTranslationWorker(
    BaseWorker[  # type: ignore
        Tuple[str, str, str, Dict[str, Any]],
        str,
        MBartTranslationConfig,
        Tuple[AutoModelForSeq2SeqLM, AutoTokenizer],
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
        config: MBartTranslationConfig,
    ) -> Tuple[AutoModelForSeq2SeqLM, AutoTokenizer]:
        model = AutoModelForSeq2SeqLM.from_pretrained(
            config.model_name,
            cache_dir=config.model_download_path,
        ).to(config.device)
        tokenizer = AutoTokenizer.from_pretrained(
            config.model_name,
            cache_dir=config.model_download_path,
        )
        return model, tokenizer

    def handle_command(
        self,
        command: str,
        args: Tuple[str, str, str, Dict[str, Any]],
        shared_object: Tuple[AutoModelForSeq2SeqLM, AutoTokenizer],
        config: MBartTranslationConfig,
        pipe: multiprocessing.connection.Connection,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        if command == "translate":
            try:
                with processing_lock:
                    is_processing.value = True

                text, source_language, target_language, translation_parameters = args
                model, tokenizer = shared_object

                tokenizer.src_lang = source_language
                inputs = tokenizer(text, return_tensors="pt")
                inputs = {key: tensor.to(config.device) for key, tensor in inputs.items()}

                if "forced_bos_token_id" not in translation_parameters:
                    translation_parameters["forced_bos_token_id"] = tokenizer.lang_code_to_id[target_language]

                translation = model.generate(**inputs, **translation_parameters)

                output = [tokenizer.decode(t, skip_special_tokens=True) for t in translation]

                pipe.send("".join(output))

            except Exception as e:
                pipe.send(e)

            finally:
                with processing_lock:
                    is_processing.value = False

    def get_worker_name(self) -> str:
        return type(self).__name__
