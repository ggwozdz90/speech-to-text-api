import logging
from typing import Optional


class Logger:
    _instance: Optional["Logger"] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self.logger = logging.getLogger("speach_to_text_api")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)
        self._configure_uvicorn_loggers()

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

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)
