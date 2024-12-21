from typing import Annotated, List

from fastapi import Depends

from config.app_config import AppConfig
from config.logger_config import Logger
from data.repositories.translation_model_repository_impl import (
    TranslationModelRepositoryImpl,
)
from domain.models.sentence_model import SentenceModel
from domain.repositories.translation_model_repository import TranslationModelRepository


class TranslationService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        translation_model_repository: Annotated[TranslationModelRepository, Depends(TranslationModelRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
    ) -> None:
        self.config = config
        self.translation_model_repository = translation_model_repository
        self.logger = logger

    def translate_sentences(
        self,
        sentences: List[SentenceModel],
        source_language: str,
        target_language: str,
    ) -> None:
        self.logger.info(f"Translating sentences from {source_language} to {target_language}")

        for i, sentence in enumerate(sentences):
            self.logger.info(f"Translating sentence {i + 1} of {len(sentences)}")

            sentence.text = self.translation_model_repository.translate(
                sentence.text,
                source_language,
                target_language,
            )

        self.logger.info("Translation of sentences completed")

    def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        self.logger.info(f"Translating text from {source_language} to {target_language}")

        translated_text: str = self.translation_model_repository.translate(
            text,
            source_language,
            target_language,
        )

        self.logger.info("Translation of text completed")
        return translated_text
