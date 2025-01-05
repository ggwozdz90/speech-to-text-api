from typing import Annotated

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.workers.whisper_speech_to_text_worker import (
    WhisperSpeechToTextConfig,
    WhisperSpeechToTextWorker,
)
from domain.exceptions.unsupported_model_configuration_error import (
    UnsupportedModelConfigurationError,
)


class SpeechToTextWorkerFactory:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        logger: Annotated[Logger, Depends()],
    ):
        self.config = config
        self.logger = logger

    def create(self) -> WhisperSpeechToTextWorker:
        if self.config.speech_to_text_model_name == "openai/whisper":
            return WhisperSpeechToTextWorker(
                WhisperSpeechToTextConfig(
                    device=self.config.device,
                    model_type=self.config.speech_to_text_model_type,
                    model_download_path=self.config.speech_to_text_model_download_path,
                    log_level=self.config.log_level,
                ),
                logger=self.logger,
            )
        else:
            raise UnsupportedModelConfigurationError(self.config.speech_to_text_model_name)
