from typing import Annotated

from fastapi import Depends

from config.app_config import AppConfig
from data.repositories.whisper_repository_impl import WhisperRepositoryImpl
from domain.repositories.whisper_repository import WhisperRepository


class TranscriptionService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        whisper_repository: Annotated[WhisperRepository, Depends(WhisperRepositoryImpl)],
    ) -> None:
        self.config = config
        self.whisper_repository = whisper_repository

    def transcribe(
        self,
        file_path: str,
        language: str,
    ) -> str:
        result = self.whisper_repository.transcribe(file_path, language=language)

        return str(result["text"])
