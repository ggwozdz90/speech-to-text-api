import multiprocessing

from api.server import APIServer
from core.config.app_config import AppConfig


def main(
    config: AppConfig,
    server: APIServer,
) -> None:
    config.load_config()
    config.print_config()
    server.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    config = AppConfig()
    server = APIServer(config)
    main(config, server)
