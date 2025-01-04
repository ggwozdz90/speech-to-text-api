from typing import Annotated

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.repositories.file_repository_impl import FileRepositoryImpl
from data.repositories.speach_to_text_repository_impl import SpeachToTextRepositoryImpl
from domain.models.transcription_result_model import TranscriptionResultModel
from domain.repositories.file_repository import FileRepository
from domain.repositories.speach_to_text_repository import SpeachToTextRepository
from domain.services.language_mapping_service import LanguageMappingService


class TranscriptionService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        speach_to_text_repository: Annotated[SpeachToTextRepository, Depends(SpeachToTextRepositoryImpl)],
        file_repository: Annotated[FileRepository, Depends(FileRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
        language_mapping_service: Annotated[LanguageMappingService, Depends()],
    ) -> None:
        self.config = config
        self.speach_to_text_repository = speach_to_text_repository
        self.file_repository = file_repository
        self.logger = logger
        self.language_mapping_service = language_mapping_service

    async def transcribe(
        self,
        file: UploadFile,
        language: str,
    ) -> TranscriptionResultModel:
        file_path = await self.file_repository.save_file(file)

        language_mapped = self.language_mapping_service.map_language(
            language,
            self.config.speach_to_text_model_name,
        )

        self.logger.debug(f"Starting transcription for file '{file.filename}' with language '{language_mapped}'")

        result = self.speach_to_text_repository.transcribe(
            file_path,
            language=language_mapped,
        )
        self.logger.debug(f"Completed transcription for file '{file.filename}'")

        if self.config.delete_files_after_transcription:
            self.file_repository.delete_file(file_path)

        transcription_result = TranscriptionResultModel(**result)

        return transcription_result
