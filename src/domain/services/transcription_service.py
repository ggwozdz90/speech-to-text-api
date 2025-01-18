from typing import Annotated, Any, Dict

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.repositories.file_repository_impl import FileRepositoryImpl
from data.repositories.speech_to_text_repository_impl import SpeechToTextRepositoryImpl
from domain.models.transcription_result_model import TranscriptionResultModel
from domain.repositories.file_repository import FileRepository
from domain.repositories.speech_to_text_repository import SpeechToTextRepository
from domain.services.language_mapping_service import LanguageMappingService


class TranscriptionService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        speech_to_text_repository: Annotated[SpeechToTextRepository, Depends(SpeechToTextRepositoryImpl)],
        file_repository: Annotated[FileRepository, Depends(FileRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
        language_mapping_service: Annotated[LanguageMappingService, Depends()],
    ) -> None:
        self.config = config
        self.speech_to_text_repository = speech_to_text_repository
        self.file_repository = file_repository
        self.logger = logger
        self.language_mapping_service = language_mapping_service

    async def transcribe(
        self,
        file: UploadFile,
        language: str,
        transcription_parameters: Dict[str, Any],
    ) -> TranscriptionResultModel:
        file_path = await self.file_repository.save_file(file)

        language_mapped = self.language_mapping_service.map_language(
            language,
            self.config.speech_to_text_model_name,
        )

        self.logger.debug(f"Starting transcription for file '{file.filename}' with language '{language_mapped}'")

        result = self.speech_to_text_repository.transcribe(
            file_path,
            language_mapped,
            transcription_parameters,
        )
        self.logger.debug(f"Completed transcription for file '{file.filename}'")

        if self.config.delete_files_after_transcription:
            self.file_repository.delete_file(file_path)

        transcription_result = TranscriptionResultModel(**result)

        return transcription_result
