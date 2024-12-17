from typing import Annotated

import whisper
from fastapi import Depends

from config.app_config import AppConfig
from data.repositories.directory_repository_impl import DirectoryRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository
from domain.repositories.whisper_repository import WhisperRepository


class WhisperRepositoryImpl(WhisperRepository):  # type: ignore
    _instance = None

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
        directory_repository: Annotated[DirectoryRepository, Depends(DirectoryRepositoryImpl)],
    ) -> "WhisperRepositoryImpl":
        if cls._instance is None:
            cls._instance = super(WhisperRepositoryImpl, cls).__new__(cls)
            cls._instance._initialize(config, directory_repository)
        return cls._instance  # type: ignore

    def _initialize(
        self,
        config: AppConfig,
        directory_repository: DirectoryRepository,
    ) -> None:
        directory_repository.create_directory(config.whisper_model_download_path)

        self.model = whisper.load_model(
            config.whisper_model_name,
            download_root=config.whisper_model_download_path,
        )

    def transcribe(
        self,
        file_path: str,
        language: str,
    ) -> dict[str, str]:
        if self.model is None:
            raise ValueError("Model is not initialized")

        result = self.model.transcribe(
            file_path,
            language=language,
        )

        return result  # type: ignore
