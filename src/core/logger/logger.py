import inspect
import logging
from typing import Optional


class Logger:
    _instance: Optional["Logger"] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()

        return cls._instance

    def _configure_uvicorn_loggers(self) -> None:
        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_logger.handlers = []
        uvicorn_logger.setLevel(self.logger.level)
        uvicorn_logger.propagate = False

        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.handlers = []
        uvicorn_access_logger.setLevel(self.logger.level)
        uvicorn_access_logger.propagate = False

        for handler in self.logger.handlers:
            uvicorn_logger.addHandler(handler)
            uvicorn_access_logger.addHandler(handler)

    def _initialize(self) -> None:
        self.logger = logging.getLogger("{{{PROJECT-NAME}}}")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)
        self._configure_uvicorn_loggers()

    def _log(self, level: int, message: str) -> None:
        caller = inspect.stack()[2]
        module = inspect.getmodule(caller[0])
        module_name = module.__name__ if module else "unknown_module"
        log_message = f"{module_name}.{caller.function} - {message}"
        self.logger.log(level, log_message)

    def info(self, message: str) -> None:
        self._log(logging.INFO, message)

    def error(self, message: str) -> None:
        self._log(logging.ERROR, message)

    def debug(self, message: str) -> None:
        self._log(logging.DEBUG, message)

    def warning(self, message: str) -> None:
        self._log(logging.WARNING, message)

    def set_level(self, log_level: str) -> None:
        self.info(f"Setting log level to {log_level}")

        self.logger.setLevel(log_level)

        for handler in self.logger.handlers:
            handler.setLevel(log_level)

        self._configure_uvicorn_loggers()

        self.info("Log level set successfully.")
