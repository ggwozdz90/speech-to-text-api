import multiprocessing
import multiprocessing.connection
import multiprocessing.synchronize
from dataclasses import dataclass
from multiprocessing.sharedctypes import Synchronized
from typing import Tuple

import torch
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
        Tuple[str, str, str],
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
    ) -> str:
        if not self.is_alive():
            raise WorkerNotRunningError()

        self._pipe_parent.send(("translate", (text, source_language, target_language)))
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
        args: Tuple[str, str, str],
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

                text, source_language, target_language = args
                model, tokenizer = shared_object

                tokenizer.src_lang = source_language
                inputs = tokenizer([text], truncation=True, padding=True, max_length=1024, return_tensors="pt")

                for key in inputs:
                    inputs[key] = inputs[key].to(config.device)

                with torch.no_grad():
                    kwargs = {"forced_bos_token_id": tokenizer.lang_code_to_id[target_language]}

                    translated = model.generate(**inputs, num_beams=5, **kwargs)

                    output = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

                pipe.send("".join(output))

            except Exception as e:
                pipe.send(e)

            finally:
                with processing_lock:
                    is_processing.value = False

    def get_worker_name(self) -> str:
        return type(self).__name__
