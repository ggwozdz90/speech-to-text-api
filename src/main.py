import multiprocessing

from api.server import APIServer
from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.cuda.cuda_checker import CudaChecker


def main(
    logger: Logger,
    config: AppConfig,
    cuda_checker: CudaChecker,
    server: APIServer,
) -> None:
    logger.info("Starting the Speech-to-Text API server...")
    config.initialize(logger)
    logger.set_level(config.log_level)
    cuda_checker.check_cuda_support()
    server.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    logger = Logger()
    config = AppConfig()
    cuda_checker = CudaChecker(logger)
    server = APIServer(config, logger)
    main(logger, config, cuda_checker, server)
