from typing import Annotated

from fastapi import Depends, UploadFile

from config.app_config import AppConfig
from data.repositories.file_repository_impl import FileRepositoryImpl
from domain.repositories.file_repository import FileRepository
from domain.services.subtitle_service import SubtitleService
from domain.services.transcription_service import TranscriptionService


class TranscribeFileToSrtUseCase:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        transcription_service: Annotated[TranscriptionService, Depends()],
        file_repository: Annotated[FileRepository, Depends(FileRepositoryImpl)],
        subtitle_service: Annotated[SubtitleService, Depends()],
    ) -> None:
        self.config = config
        self.transcription_service = transcription_service
        self.file_repository = file_repository
        self.subtitle_service = subtitle_service

    async def execute(
        self,
        file: UploadFile,
        language: str,
    ) -> str:
        file_path = await self.file_repository.save_file(file)
        result = self.transcription_service.transcribe(file_path, language)

        if self.config.delete_files_after_transcription:
            self.file_repository.delete_file(file_path)

        srt_result = self.subtitle_service.convert_to_srt(result)

        return srt_result  # type: ignore
