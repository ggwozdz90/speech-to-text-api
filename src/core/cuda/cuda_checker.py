import torch

from core.logger.logger import Logger


class CudaChecker:
    def __init__(
        self,
        logger: Logger,
    ) -> None:
        self.logger = logger

    def check_cuda_support(self) -> None:
        if torch.cuda.is_available():
            cuda_devices = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
            self.logger.info(f"CUDA is supported. Available devices: {', '.join(cuda_devices)}")
        else:
            self.logger.info("CUDA is not supported on this device.")
