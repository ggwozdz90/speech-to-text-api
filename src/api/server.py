import uvicorn
from fastapi import FastAPI

from api.middlewares.process_time_middleware import ProcessTimeMiddleware
from api.routers.transcribe_router import TranscribeRouter
from core.config.app_config import AppConfig
from core.logger.logger import Logger


class APIServer:
    def __init__(
        self,
        config: AppConfig,
        logger: Logger,
    ) -> None:
        self.config = config
        self.app = FastAPI()
        self.app.add_middleware(ProcessTimeMiddleware, logger=logger)
        self.app.include_router(TranscribeRouter().router)

    def start(self) -> None:
        uvicorn.run(
            self.app,
            host=self.config.fastapi_host,
            port=self.config.fastapi_port,
            server_header=False,
        )
