from typing import Annotated, Union

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.workers.mbart_translation_worker import (
    MBartTranslationConfig,
    MBartTranslationWorker,
)
from data.workers.seamless_translation_worker import (
    SeamlessTranslationConfig,
    SeamlessTranslationWorker,
)
from domain.exceptions.unsupported_model_configuration_error import (
    UnsupportedModelConfigurationError,
)


class TranslationWorkerFactory:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        logger: Annotated[Logger, Depends()],
    ):
        self.config = config
        self.logger = logger

    def create(self) -> Union[MBartTranslationWorker, SeamlessTranslationWorker]:
        if self.config.translation_model_name == "facebook/mbart-large-50-many-to-many-mmt":
            return MBartTranslationWorker(
                MBartTranslationConfig(
                    device=self.config.device,
                    model_name=self.config.translation_model_name,
                    model_download_path=self.config.translation_model_download_path,
                    log_level=self.config.log_level,
                ),
                logger=self.logger,
            )
        elif self.config.translation_model_name == "facebook/seamless-m4t-v2-large":
            return SeamlessTranslationWorker(
                SeamlessTranslationConfig(
                    device=self.config.device,
                    model_name=self.config.translation_model_name,
                    model_download_path=self.config.translation_model_download_path,
                    log_level=self.config.log_level,
                ),
                logger=self.logger,
            )
        else:
            raise UnsupportedModelConfigurationError(self.config.translation_model_name)
