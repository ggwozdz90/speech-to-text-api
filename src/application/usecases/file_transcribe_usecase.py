from typing import Annotated

from fastapi import Depends, UploadFile

from config.app_config import AppConfig
from domain.services.file_service import FileService
from domain.services.transcription_service import TranscriptionService


class FileTranscribeUseCase:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        transcription_service: Annotated[TranscriptionService, Depends()],
        file_service: Annotated[FileService, Depends()],
    ) -> None:
        self.config = config
        self.transcription_service = transcription_service
        self.file_service = file_service

    async def execute(
        self,
        file: UploadFile,
        language: str,
    ) -> str:
        file_path = await self.file_service.save_file(file)
        result = self.transcription_service.transcribe(file_path, language)

        if self.config.delete_files_after_transcription:
            self.file_service.delete_file(file_path)

        return result  # type: ignore
