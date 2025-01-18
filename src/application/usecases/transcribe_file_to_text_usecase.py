from typing import Annotated, Any, Dict, Optional

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.services.transcription_service import TranscriptionService
from domain.services.translation_service import TranslationService


class TranscribeFileToTextUseCase:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        logger: Annotated[Logger, Depends()],
        transcription_service: Annotated[TranscriptionService, Depends()],
        translation_service: Annotated[TranslationService, Depends()],
    ) -> None:
        self.config = config
        self.logger = logger
        self.transcription_service = transcription_service
        self.translation_service = translation_service

    async def execute(
        self,
        file: UploadFile,
        source_language: str,
        target_language: Optional[str],
        transcription_parameters: Dict[str, Any],
        translation_parameters: Dict[str, Any],
    ) -> str:
        self.logger.info(
            f"Executing transcription for file '{file.filename}' from '{source_language}' to '{target_language}'",
        )

        transcription_result = await self.transcription_service.transcribe(
            file,
            source_language,
            transcription_parameters,
        )

        if not target_language or source_language == target_language:
            self.logger.info(f"Returning transcription result for file '{file.filename}'")

            return str(transcription_result.text)

        translation_result: str = self.translation_service.translate_text(
            transcription_result.text,
            source_language,
            target_language,
            translation_parameters,
        )

        self.logger.info(f"Returning translation result for file '{file.filename}'")

        return translation_result
