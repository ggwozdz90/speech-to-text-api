import threading
import time
from typing import Annotated, Optional

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.timer.timer import TimerFactory
from data.factories.speach_to_text_worker_factory import SpeachToTextWorkerFactory
from data.repositories.directory_repository_impl import DirectoryRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository
from domain.repositories.speach_to_text_repository import SpeachToTextRepository


class SpeachToTextRepositoryImpl(SpeachToTextRepository):  # type: ignore
    _instance: Optional["SpeachToTextRepositoryImpl"] = None
    _lock = threading.Lock()

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
        directory_repository: Annotated[DirectoryRepository, Depends(DirectoryRepositoryImpl)],
        timer_factory: Annotated[TimerFactory, Depends()],
        logger: Annotated[Logger, Depends()],
        worker_factory: Annotated[SpeachToTextWorkerFactory, Depends()],
    ) -> "SpeachToTextRepositoryImpl":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SpeachToTextRepositoryImpl, cls).__new__(cls)
                    cls._instance._initialize(config, directory_repository, timer_factory, logger, worker_factory)

        return cls._instance

    def _initialize(
        self,
        config: AppConfig,
        directory_repository: DirectoryRepository,
        timer_factory: TimerFactory,
        logger: Logger,
        worker_factory: SpeachToTextWorkerFactory,
    ) -> None:
        directory_repository.create_directory(config.speach_to_text_model_download_path)
        self.config = config
        self.timer = timer_factory.create()
        self.logger = logger
        self.worker = worker_factory.create()
        self.last_access_time = 0.0

    def transcribe(
        self,
        file_path: str,
        language: str,
    ) -> dict[str, str]:
        with self._lock:
            if not self.worker.is_alive():
                self.logger.info("Starting speach to text worker")
                self.worker.start()

        self.logger.debug(f"Transcribing file: {file_path}, language: {language}")

        result: dict[str, str] = self.worker.transcribe(
            file_path,
            language,
        )

        self.timer.start(
            self.config.model_idle_timeout,
            self._check_idle_timeout,
        )

        self.last_access_time = time.time()

        self.logger.debug(f"Transcription completed for file: {file_path}, language: {language}")

        return result

    def _check_idle_timeout(self) -> None:
        self.logger.debug("Checking speach to text model idle timeout")

        if self.worker.is_alive() and not self.worker.is_processing():
            with self._lock:
                self.worker.stop()
                self.timer.cancel()
                self.logger.info("Speach to text model stopped due to idle timeout")
