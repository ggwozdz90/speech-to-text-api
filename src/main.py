from api.server import APIServer
from config.app_config import AppConfig


def main(
    config: AppConfig,
    server: APIServer,
) -> None:
    config.load_config()
    config.print_config()
    server.start()


if __name__ == "__main__":
    config = AppConfig()
    server = APIServer(config)
    main(config, server)
