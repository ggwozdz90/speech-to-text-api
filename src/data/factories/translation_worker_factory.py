from typing import Annotated, Union

from fastapi import Depends

from core.config.app_config import AppConfig
from data.workers.mbart_worker import MBartConfig, MBartWorker
from data.workers.seamless_worker import SeamlessConfig, SeamlessWorker


class TranslationWorkerFactory:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
    ):
        self.config = config

    def create(self) -> Union[MBartWorker, SeamlessWorker]:
        if self.config.translation_model_name == "facebook/mbart-large-50-many-to-many-mmt":
            return MBartWorker(
                MBartConfig(
                    device=self.config.device,
                    model_name=self.config.translation_model_name,
                    model_download_path=self.config.translation_model_download_path,
                )
            )
        elif self.config.translation_model_name == "facebook/seamless-m4t-v2-large":
            return SeamlessWorker(
                SeamlessConfig(
                    device=self.config.device,
                    model_name=self.config.translation_model_name,
                    model_download_path=self.config.translation_model_download_path,
                )
            )
        else:
            raise ValueError(f"Unsupported translation model name: {self.config.translation_model_name}")
