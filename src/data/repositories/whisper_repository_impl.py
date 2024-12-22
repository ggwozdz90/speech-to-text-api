import threading
import time
from typing import Annotated, Optional

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.timer.timer import Timer
from data.repositories.directory_repository_impl import DirectoryRepositoryImpl
from data.workers.whisper_worker import WhisperWorker
from domain.repositories.directory_repository import DirectoryRepository
from domain.repositories.whisper_repository import WhisperRepository


class WhisperRepositoryImpl(WhisperRepository):  # type: ignore
    _instance: Optional["WhisperRepositoryImpl"] = None
    _lock = threading.Lock()

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
        directory_repository: Annotated[DirectoryRepository, Depends(DirectoryRepositoryImpl)],
        timer: Annotated[Timer, Depends()],
        logger: Annotated[Logger, Depends()],
        worker: Annotated[WhisperWorker, Depends()],
    ) -> "WhisperRepositoryImpl":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(WhisperRepositoryImpl, cls).__new__(cls)
                    cls._instance._initialize(config, directory_repository, timer, logger, worker)
        return cls._instance

    def _initialize(
        self,
        config: AppConfig,
        directory_repository: DirectoryRepository,
        timer: Timer,
        logger: Logger,
        worker: WhisperWorker,
    ) -> None:
        directory_repository.create_directory(config.whisper_model_download_path)
        self.config = config
        self.timer = timer
        self.logger = logger
        self.worker = worker
        self.last_access_time = 0.0

    def transcribe(
        self,
        file_path: str,
        language: str,
    ) -> dict[str, str]:
        with self._lock:
            if not self.worker.is_alive():
                self.worker.start(
                    self.config.device,
                    self.config.whisper_model_name,
                    self.config.whisper_model_download_path,
                )

        result: dict[str, str] = self.worker.transcribe(
            file_path,
            language,
        )

        self.timer.start(
            self.config.model_idle_timeout,
            self._check_idle_timeout,
        )

        self.last_access_time = time.time()

        return result

    def _check_idle_timeout(self) -> None:
        self.logger.info("Checking whisper model idle timeout")

        if self.worker.is_alive() and not self.worker.is_processing():
            with self._lock:
                self.worker.stop()
                self.timer.cancel()
                self.logger.info("Whisper model stopped due to idle timeout")
