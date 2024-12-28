import logging
from unittest.mock import patch

import pytest

from src.core.logger.logger import Logger


@pytest.fixture
def logger_instance() -> Logger:
    return Logger()


def test_info_logs_message(logger_instance: Logger) -> None:
    # Given
    message = "Test info message"

    with patch.object(logger_instance.logger, "info") as mock_info:
        # When
        logger_instance.info(message)

        # Then
        mock_info.assert_called_once_with(message)


def test_error_logs_message(logger_instance: Logger) -> None:
    # Given
    message = "Test error message"

    with patch.object(logger_instance.logger, "error") as mock_error:
        # When
        logger_instance.error(message)

        # Then
        mock_error.assert_called_once_with(message)


def test_logger_is_singleton() -> None:
    # Given
    logger1 = Logger()
    logger2 = Logger()

    # Then
    assert logger1 is logger2


def test_logger_initialization() -> None:
    # Given
    logger_instance = Logger()

    # Then
    assert logger_instance.logger.name == "speach_to_text_api"
    assert logger_instance.logger.level == logging.INFO
    assert len(logger_instance.logger.handlers) > 0
    assert isinstance(logger_instance.logger.handlers[0], logging.StreamHandler)
