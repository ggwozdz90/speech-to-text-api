import threading
import time
from typing import Annotated, Optional

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.timer.timer import TimerFactory
from data.factories.translation_worker_factory import TranslationWorkerFactory
from data.repositories.directory_repository_impl import DirectoryRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository
from domain.repositories.translation_model_repository import TranslationModelRepository


class TranslationModelRepositoryImpl(TranslationModelRepository):  # type: ignore
    _instance: Optional["TranslationModelRepositoryImpl"] = None
    _lock = threading.Lock()

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
        directory_repository: Annotated[DirectoryRepository, Depends(DirectoryRepositoryImpl)],
        timer_factory: Annotated[TimerFactory, Depends()],
        logger: Annotated[Logger, Depends()],
        worker_factory: Annotated[TranslationWorkerFactory, Depends()],
    ) -> "TranslationModelRepositoryImpl":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(TranslationModelRepositoryImpl, cls).__new__(cls)
                    cls._instance._initialize(config, directory_repository, timer_factory, logger, worker_factory)

        return cls._instance

    def _initialize(
        self,
        config: AppConfig,
        directory_repository: DirectoryRepository,
        timer_factory: TimerFactory,
        logger: Logger,
        worker_factory: TranslationWorkerFactory,
    ) -> None:
        directory_repository.create_directory(config.translation_model_download_path)
        self.config = config
        self.timer = timer_factory.create()
        self.logger = logger
        self.worker = worker_factory.create()
        self.last_access_time = 0.0

    def _check_idle_timeout(self) -> None:
        self.logger.debug("Checking translation model idle timeout")

        if self.worker.is_alive() and not self.worker.is_processing():
            with self._lock:
                self.worker.stop()
                self.timer.cancel()
                self.logger.info("Translation model stopped due to idle timeout")

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        with self._lock:
            if not self.worker.is_alive():
                self.logger.info("Starting translation worker")
                self.worker.start()

        self.logger.debug(
            f"Translating started from source_language: {source_language}, target_language: {target_language}",
        )

        result: str = self.worker.translate(
            text,
            source_language,
            target_language,
        )

        self.timer.start(
            self.config.model_idle_timeout,
            self._check_idle_timeout,
        )

        self.last_access_time = time.time()

        self.logger.debug(
            f"Translating completed from source_language: {source_language}, target_language: {target_language}",
        )

        return result
