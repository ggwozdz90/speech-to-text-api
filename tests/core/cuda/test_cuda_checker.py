from unittest.mock import Mock, patch

import pytest

from core.cuda.cuda_checker import CudaChecker
from core.logger.logger import Logger


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


def test_cuda_checker_initialization(mock_logger: Logger) -> None:
    # Given / When
    cuda_checker = CudaChecker(logger=mock_logger)

    # Then
    assert cuda_checker.logger == mock_logger


def test_check_cuda_support_with_cuda_available(mock_logger: Logger) -> None:
    # Given
    cuda_checker = CudaChecker(logger=mock_logger)
    with (
        patch("torch.cuda.is_available", return_value=True),
        patch("torch.cuda.device_count", return_value=2),
        patch("torch.cuda.get_device_name", side_effect=["Device1", "Device2"]),
    ):

        # When
        cuda_checker.check_cuda_support()

        # Then
        mock_logger.info.assert_called_once_with("CUDA is supported. Available devices: Device1, Device2")


def test_check_cuda_support_without_cuda_available(mock_logger: Logger) -> None:
    # Given
    cuda_checker = CudaChecker(logger=mock_logger)
    with patch("torch.cuda.is_available", return_value=False):

        # When
        cuda_checker.check_cuda_support()

        # Then
        mock_logger.info.assert_called_once_with("CUDA is not supported on this device.")
