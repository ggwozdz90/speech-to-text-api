import multiprocessing
import multiprocessing.connection
import multiprocessing.synchronize
from abc import ABC, abstractmethod
from multiprocessing.sharedctypes import Synchronized
from typing import Generic, Optional, TypeVar

from core.logger.logger import Logger

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")
ConfigType = TypeVar("ConfigType")
SharedObjectType = TypeVar("SharedObjectType")


class BaseWorker(
    ABC,
    Generic[
        InputType,
        OutputType,
        ConfigType,
        SharedObjectType,
    ],
):
    def __init__(
        self,
        config: ConfigType,
        logger: Logger,
    ) -> None:
        self._config = config
        self._logger = logger
        self._process: Optional[multiprocessing.Process] = None
        self._is_processing: Synchronized = multiprocessing.Value("b", False)  # type: ignore
        self._processing_lock: multiprocessing.synchronize.Lock = multiprocessing.Lock()
        self._pipe_parent, self._pipe_child = multiprocessing.Pipe()
        self._stop_event = multiprocessing.Event()

    @abstractmethod
    def initialize_shared_object(
        self,
        config: ConfigType,
    ) -> SharedObjectType:
        pass

    @abstractmethod
    def handle_command(
        self,
        command: str,
        args: InputType,
        shared_object: SharedObjectType,
        config: ConfigType,
        pipe: multiprocessing.connection.Connection,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        pass

    @abstractmethod
    def get_worker_name(self) -> str:
        pass

    def _run_process(
        self,
        config: ConfigType,
        pipe: multiprocessing.connection.Connection,
        stop_event: multiprocessing.synchronize.Event,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        try:
            self._logger.set_level(config.log_level)  # type: ignore
            self._logger.info(f"{self.get_worker_name()} started with PID: {multiprocessing.current_process().pid}")
            shared_object = self.initialize_shared_object(config)

            while not stop_event.is_set():
                if pipe.poll(timeout=1):
                    command, args = pipe.recv()
                    self._logger.debug(f"{self.get_worker_name()} received command: {command} with args: {args}")
                    self.handle_command(command, args, shared_object, config, pipe, is_processing, processing_lock)
                    self._logger.debug(f"{self.get_worker_name()} command: {command} processed")

        finally:
            del shared_object
            pipe.close()
            self._logger.info(f"{self.get_worker_name()} stopped with PID: {multiprocessing.current_process().pid}")

    def start(self) -> None:
        if self._process is None or not self._process.is_alive():
            self._stop_event.clear()
            self._process = multiprocessing.Process(
                target=self._run_process,
                args=(
                    self._config,
                    self._pipe_child,
                    self._stop_event,
                    self._is_processing,
                    self._processing_lock,
                ),
            )
            self._process.start()

    def stop(self) -> None:
        if self._process and self._process.is_alive():
            self._stop_event.set()
            self._process.join(timeout=5)

            if self._process.is_alive():
                self._process.terminate()

            self._process = None

    def is_alive(self) -> bool:
        return self._process is not None and self._process.is_alive()

    def is_processing(self) -> bool:
        return bool(self._is_processing.value)
