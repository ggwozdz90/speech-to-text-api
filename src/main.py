import multiprocessing

from api.server import APIServer
from core.config.app_config import AppConfig
from core.cuda.cuda_checker import CudaChecker
from core.logger.logger import Logger


def main(
    logger: Logger,
    config: AppConfig,
    cuda_checker: CudaChecker,
    server: APIServer,
) -> None:
    logger.info("Starting the speech-to-text-api server...")
    config.initialize(logger)
    logger.set_level(config.log_level)
    cuda_checker.check_cuda_support()
    server.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn", force=True)
    logger = Logger()
    config = AppConfig()
    cuda_checker = CudaChecker(logger)
    server = APIServer(config, logger)
    main(logger, config, cuda_checker, server)
