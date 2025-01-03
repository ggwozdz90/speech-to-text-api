import multiprocessing

from api.server import APIServer
from core.config.app_config import AppConfig
from core.logger.logger import Logger


def main(
    config: AppConfig,
    server: APIServer,
) -> None:
    config.load_config()
    config.print_config()
    server.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    logger = Logger()
    config = AppConfig()
    server = APIServer(config, logger)
    main(config, server)
