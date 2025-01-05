from typing import Annotated

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.workers.whisper_speach_to_text_worker import (
    WhisperSpeachToTextConfig,
    WhisperSpeachToTextWorker,
)
from domain.exceptions.unsupported_model_configuration_error import (
    UnsupportedModelConfigurationError,
)


class SpeachToTextWorkerFactory:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        logger: Annotated[Logger, Depends()],
    ):
        self.config = config
        self.logger = logger

    def create(self) -> WhisperSpeachToTextWorker:
        if self.config.speach_to_text_model_name == "openai/whisper":
            return WhisperSpeachToTextWorker(
                WhisperSpeachToTextConfig(
                    device=self.config.device,
                    model_type=self.config.speach_to_text_model_type,
                    model_download_path=self.config.speach_to_text_model_download_path,
                    log_level=self.config.log_level,
                ),
                logger=self.logger,
            )
        else:
            raise UnsupportedModelConfigurationError(self.config.speach_to_text_model_name)
