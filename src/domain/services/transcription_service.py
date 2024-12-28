from typing import Annotated

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.repositories.file_repository_impl import FileRepositoryImpl
from data.repositories.speach_to_text_repository_impl import SpeachToTextRepositoryImpl
from domain.models.transcription_result_model import TranscriptionResultModel
from domain.repositories.file_repository import FileRepository
from domain.repositories.speach_to_text_repository import SpeachToTextRepository


class TranscriptionService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        speach_to_text_repository: Annotated[SpeachToTextRepository, Depends(SpeachToTextRepositoryImpl)],
        file_repository: Annotated[FileRepository, Depends(FileRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
    ) -> None:
        self.config = config
        self.speach_to_text_repository = speach_to_text_repository
        self.file_repository = file_repository
        self.logger = logger

    async def transcribe(
        self,
        file: UploadFile,
        language: str,
    ) -> TranscriptionResultModel:
        file_path = await self.file_repository.save_file(file)
        self.logger.info(f"File saved at: {file_path}")

        self.logger.info(f"Starting transcription for file: {file.filename}")
        result = self.speach_to_text_repository.transcribe(file_path, language=language)
        self.logger.info("Transcription completed")

        if self.config.delete_files_after_transcription:
            self.file_repository.delete_file(file_path)
            self.logger.info(f"File deleted: {file_path}")

        transcription_result = TranscriptionResultModel(**result)

        return transcription_result
