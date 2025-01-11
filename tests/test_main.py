from unittest.mock import Mock, patch

import pytest

from api.server import APIServer
from core.config.app_config import AppConfig
from core.logger.logger import Logger
from src.main import main


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_server() -> APIServer:
    return Mock(APIServer)


def test_main(
    mock_logger: Logger,
    mock_config: AppConfig,
    mock_server: APIServer,
) -> None:
    # Given
    mock_config.log_level = "INFO"
    with patch.object(mock_config, "initialize") as mock_initialize, patch.object(mock_server, "start") as mock_start:

        # When
        main(mock_logger, mock_config, mock_server)

        # Then
        mock_initialize.assert_called_once()
        mock_start.assert_called_once()


def test_main_load_config_exception(
    mock_logger: Logger,
    mock_config: AppConfig,
    mock_server: APIServer,
) -> None:
    # Given
    with (
        patch.object(mock_config, "initialize", side_effect=Exception("Initialize error")),
        patch.object(
            mock_server,
            "start",
        ) as mock_start,
    ):

        # When / Then
        with pytest.raises(Exception, match="Initialize error"):
            main(mock_logger, mock_config, mock_server)

        mock_start.assert_not_called()


def test_main_start_exception(
    mock_logger: Logger,
    mock_config: AppConfig,
    mock_server: APIServer,
) -> None:
    # Given
    mock_config.log_level = "INFO"
    with (
        patch.object(mock_config, "initialize") as mock_load_config,
        patch.object(
            mock_server,
            "start",
            side_effect=Exception("Start error"),
        ),
    ):

        # When / Then
        with pytest.raises(Exception, match="Start error"):
            main(mock_logger, mock_config, mock_server)

        mock_load_config.assert_called_once()
