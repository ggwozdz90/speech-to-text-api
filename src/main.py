import multiprocessing

from api.server import APIServer
from core.config.app_config import AppConfig
from core.logger.logger import Logger


def main(
    logger: Logger,
    config: AppConfig,
    server: APIServer,
) -> None:
    config.initialize(logger)
    server.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    logger = Logger()
    config = AppConfig()
    server = APIServer(config, logger)
    main(logger, config, server)
