from typing import Annotated

from fastapi import Depends

from core.config.app_config import AppConfig
from data.workers.whisper_worker import WhisperConfig, WhisperWorker


class SpeachToTextWorkerFactory:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
    ):
        self.config = config

    def create(self) -> WhisperWorker:
        if self.config.speach_to_text_model_name == "openai/whisper":
            return WhisperWorker(
                WhisperConfig(
                    device=self.config.device,
                    model_type=self.config.speach_to_text_model_type,
                    model_download_path=self.config.speach_to_text_model_download_path,
                )
            )
        else:
            raise ValueError(f"Unsupported speach to text model name: {self.config.speach_to_text_model_name}")
