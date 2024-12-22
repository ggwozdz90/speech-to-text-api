from typing import Annotated, Optional

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from domain.services.transcription_service import TranscriptionService
from domain.services.translation_service import TranslationService


class TranscribeFileToTextUseCase:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        transcription_service: Annotated[TranscriptionService, Depends()],
        translation_service: Annotated[TranslationService, Depends()],
    ) -> None:
        self.config = config
        self.transcription_service = transcription_service
        self.translation_service = translation_service

    async def execute(
        self,
        file: UploadFile,
        source_language: str,
        target_language: Optional[str],
    ) -> str:
        transcription_result = await self.transcription_service.transcribe(file, source_language)

        if not target_language or source_language == target_language:
            return str(transcription_result.text)

        translation_result: str = self.translation_service.translate_text(
            transcription_result.text,
            source_language,
            target_language,
        )

        return translation_result
