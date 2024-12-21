from typing import Annotated, Optional

import torch
from fastapi import Depends
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from config.app_config import AppConfig
from data.repositories.directory_repository_impl import DirectoryRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository
from domain.repositories.translation_model_repository import TranslationModelRepository


class TranslationModelRepositoryImpl(TranslationModelRepository):  # type: ignore
    _instance: Optional["TranslationModelRepositoryImpl"] = None

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
        directory_repository: Annotated[DirectoryRepository, Depends(DirectoryRepositoryImpl)],
    ) -> "TranslationModelRepositoryImpl":
        if cls._instance is None:
            cls._instance = super(TranslationModelRepositoryImpl, cls).__new__(cls)
            cls._instance._initialize(config, directory_repository)
        return cls._instance

    def _initialize(
        self,
        config: AppConfig,
        directory_repository: DirectoryRepository,
    ) -> None:
        directory_repository.create_directory(config.translation_model_download_path)

        kwargs = {}
        kwargs["cache_dir"] = config.translation_model_download_path

        self.model = AutoModelForSeq2SeqLM.from_pretrained(config.translation_model_name, **kwargs)
        self.tokenizer = AutoTokenizer.from_pretrained(config.translation_model_name, **kwargs)

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        if self.model is None:
            raise ValueError("Model is not initialized")

        self.tokenizer.src_lang = source_language
        inputs = self.tokenizer([text], truncation=True, padding=True, max_length=1024, return_tensors="pt")

        for key in inputs:
            inputs[key] = inputs[key].to("cpu")

        with torch.no_grad():
            kwargs = {}
            kwargs["forced_bos_token_id"] = self.tokenizer.lang_code_to_id[target_language]

            translated = self.model.generate(**inputs, num_beams=5, **kwargs)

            output = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]

        return "".join(output)
