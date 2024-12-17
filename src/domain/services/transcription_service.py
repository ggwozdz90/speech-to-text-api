from typing import Annotated

from fastapi import Depends

from config.app_config import AppConfig
from data.repositories.whisper_repository_impl import WhisperRepositoryImpl
from domain.models.transcription_result_model import TranscriptionResultModel
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
    ) -> TranscriptionResultModel:
        result = self.whisper_repository.transcribe(file_path, language=language)
        transcription_result = TranscriptionResultModel(**result)

        return transcription_result
