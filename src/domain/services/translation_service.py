from typing import Annotated, List

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.repositories.translation_model_repository_impl import (
    TranslationModelRepositoryImpl,
)
from domain.models.sentence_model import SentenceModel
from domain.repositories.translation_model_repository import TranslationModelRepository
from domain.services.language_mapping_service import LanguageMappingService


class TranslationService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        translation_model_repository: Annotated[TranslationModelRepository, Depends(TranslationModelRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
        language_mapping_service: Annotated[LanguageMappingService, Depends()],
    ) -> None:
        self.config = config
        self.translation_model_repository = translation_model_repository
        self.logger = logger
        self.language_mapping_service = language_mapping_service

    def translate_sentences(
        self,
        sentences: List[SentenceModel],
        source_language: str,
        target_language: str,
    ) -> None:
        self.logger.info(f"Translating sentences from {source_language} to {target_language}")

        source_language_mapped = self.language_mapping_service.map_language(
            source_language,
            self.config.translation_model_name,
        )
        target_language_mapped = self.language_mapping_service.map_language(
            target_language,
            self.config.translation_model_name,
        )

        for i, sentence in enumerate(sentences):
            self.logger.info(f"Translating sentence {i + 1} of {len(sentences)}")

            sentence.text = self.translation_model_repository.translate(
                sentence.text,
                source_language_mapped,
                target_language_mapped,
            )

        self.logger.info("Translation of sentences completed")

    def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        source_language_mapped = self.language_mapping_service.map_language(
            source_language,
            self.config.translation_model_name,
        )
        target_language_mapped = self.language_mapping_service.map_language(
            target_language,
            self.config.translation_model_name,
        )

        self.logger.info(f"Translating text from {source_language_mapped} to {target_language_mapped}")

        translated_text: str = self.translation_model_repository.translate(
            text,
            source_language_mapped,
            target_language_mapped,
        )

        self.logger.info("Translation of text completed")
        return translated_text
