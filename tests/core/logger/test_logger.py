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

    with patch.object(logger_instance.logger, "log") as mock_info:
        # When
        logger_instance.info(message)

        # Then
        mock_info.assert_called_once_with(
            logging.INFO,
            f"tests.core.logger.test_logger.test_info_logs_message - {message}",
        )


def test_error_logs_message(logger_instance: Logger) -> None:
    # Given
    message = "Test error message"

    with patch.object(logger_instance.logger, "log") as mock_error:
        # When
        logger_instance.error(message)

        # Then
        mock_error.assert_called_once_with(
            logging.ERROR,
            f"tests.core.logger.test_logger.test_error_logs_message - {message}",
        )


def test_warning_logs_message(logger_instance: Logger) -> None:
    # Given
    message = "Test warning message"

    with patch.object(logger_instance.logger, "log") as mock_warning:
        # When
        logger_instance.warning(message)

        # Then
        mock_warning.assert_called_once_with(
            logging.WARNING,
            f"tests.core.logger.test_logger.test_warning_logs_message - {message}",
        )


def test_debug_logs_message(logger_instance: Logger) -> None:
    # Given
    message = "Test debug message"

    with patch.object(logger_instance.logger, "log") as mock_debug:
        # When
        logger_instance.debug(message)

        # Then
        mock_debug.assert_called_once_with(
            logging.DEBUG,
            f"tests.core.logger.test_logger.test_debug_logs_message - {message}",
        )


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
    assert logger_instance.logger.name == "{{{PROJECT-NAME}}}"
    assert logger_instance.logger.level == logging.INFO
    assert len(logger_instance.logger.handlers) > 0
    assert isinstance(logger_instance.logger.handlers[0], logging.StreamHandler)


def test_set_level(logger_instance: Logger) -> None:
    # Given
    log_level = "DEBUG"

    with patch.object(logger_instance.logger, "setLevel") as mock_set_level:
        # When
        logger_instance.set_level(log_level)

        # Then
        mock_set_level.assert_called_once_with(log_level)
