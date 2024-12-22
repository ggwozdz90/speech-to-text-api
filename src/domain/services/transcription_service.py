from typing import Annotated

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.repositories.file_repository_impl import FileRepositoryImpl
from data.repositories.whisper_repository_impl import WhisperRepositoryImpl
from domain.models.transcription_result_model import TranscriptionResultModel
from domain.repositories.file_repository import FileRepository
from domain.repositories.whisper_repository import WhisperRepository


class TranscriptionService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        whisper_repository: Annotated[WhisperRepository, Depends(WhisperRepositoryImpl)],
        file_repository: Annotated[FileRepository, Depends(FileRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
    ) -> None:
        self.config = config
        self.whisper_repository = whisper_repository
        self.file_repository = file_repository
        self.logger = logger

    async def transcribe(
        self,
        file: UploadFile,
        language: str,
    ) -> TranscriptionResultModel:
        self.logger.info(f"Starting transcription for file: {file.filename}")
        file_path = await self.file_repository.save_file(file)
        self.logger.info(f"File saved at: {file_path}")

        result = self.whisper_repository.transcribe(file_path, language=language)
        self.logger.info("Transcription completed")

        if self.config.delete_files_after_transcription:
            self.file_repository.delete_file(file_path)
            self.logger.info(f"File deleted: {file_path}")

        transcription_result = TranscriptionResultModel(**result)

        return transcription_result
