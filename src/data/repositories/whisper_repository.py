from typing import Annotated

import whisper
from fastapi import Depends

from config.app_config import AppConfig


class WhisperRepository:
    _instance = None

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
    ) -> "WhisperRepository":
        if cls._instance is None:
            cls._instance = super(WhisperRepository, cls).__new__(cls)
            cls._instance._initialize(config)
        return cls._instance

    def _initialize(
        self,
        config: AppConfig,
    ) -> None:
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
