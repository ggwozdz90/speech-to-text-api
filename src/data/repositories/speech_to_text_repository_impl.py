import threading
import time
from typing import Annotated, Any, Dict, Optional

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.timer.timer import TimerFactory
from data.factories.speech_to_text_worker_factory import SpeechToTextWorkerFactory
from data.repositories.directory_repository_impl import DirectoryRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository
from domain.repositories.speech_to_text_repository import SpeechToTextRepository


class SpeechToTextRepositoryImpl(SpeechToTextRepository):  # type: ignore
    _instance: Optional["SpeechToTextRepositoryImpl"] = None
    _lock = threading.Lock()

    def __new__(
        cls,
        config: Annotated[AppConfig, Depends()],
        directory_repository: Annotated[DirectoryRepository, Depends(DirectoryRepositoryImpl)],
        timer_factory: Annotated[TimerFactory, Depends()],
        logger: Annotated[Logger, Depends()],
        worker_factory: Annotated[SpeechToTextWorkerFactory, Depends()],
    ) -> "SpeechToTextRepositoryImpl":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SpeechToTextRepositoryImpl, cls).__new__(cls)
                    cls._instance._initialize(config, directory_repository, timer_factory, logger, worker_factory)

        return cls._instance

    def _initialize(
        self,
        config: AppConfig,
        directory_repository: DirectoryRepository,
        timer_factory: TimerFactory,
        logger: Logger,
        worker_factory: SpeechToTextWorkerFactory,
    ) -> None:
        directory_repository.create_directory(config.speech_to_text_model_download_path)
        self.config = config
        self.timer = timer_factory.create()
        self.logger = logger
        self.worker = worker_factory.create()
        self.last_access_time = 0.0

    def _check_idle_timeout(self) -> None:
        self.logger.debug("Checking speech to text model idle timeout")

        if self.worker.is_alive() and not self.worker.is_processing():
            with self._lock:
                self.worker.stop()
                self.timer.cancel()
                self.logger.info("Speech to text model stopped due to idle timeout")

    def transcribe(
        self,
        file_path: str,
        language: str,
        transcription_parameters: Dict[str, Any],
    ) -> dict[str, str]:
        with self._lock:
            if not self.worker.is_alive():
                self.logger.info("Starting speech to text worker")
                self.worker.start()

        self.logger.debug(f"Transcribing file: {file_path}, language: {language}")

        result: dict[str, str] = self.worker.transcribe(
            file_path,
            language,
            transcription_parameters,
        )

        self.timer.start(
            self.config.model_idle_timeout,
            self._check_idle_timeout,
        )

        self.last_access_time = time.time()

        self.logger.debug(f"Transcription completed for file: {file_path}, language: {language}")

        return result
