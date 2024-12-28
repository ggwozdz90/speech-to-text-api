from unittest.mock import Mock, patch

import pytest

from api.server import APIServer
from core.config.app_config import AppConfig
from src.main import main


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_server() -> APIServer:
    return Mock(APIServer)


def test_main(
    mock_config: AppConfig,
    mock_server: APIServer,
) -> None:
    # Given
    with patch.object(mock_config, "load_config") as mock_load_config, patch.object(
        mock_config, "print_config"
    ) as mock_print_config, patch.object(mock_server, "start") as mock_start:

        # When
        main(mock_config, mock_server)

        # Then
        mock_load_config.assert_called_once()
        mock_print_config.assert_called_once()
        mock_start.assert_called_once()


def test_main_load_config_exception(
    mock_config: AppConfig,
    mock_server: APIServer,
) -> None:
    # Given
    with patch.object(mock_config, "load_config", side_effect=Exception("Load config error")), patch.object(
        mock_config, "print_config"
    ) as mock_print_config, patch.object(mock_server, "start") as mock_start:

        # When / Then
        with pytest.raises(Exception, match="Load config error"):
            main(mock_config, mock_server)
        mock_print_config.assert_not_called()
        mock_start.assert_not_called()


def test_main_start_exception(
    mock_config: AppConfig,
    mock_server: APIServer,
) -> None:
    # Given
    with patch.object(mock_config, "load_config") as mock_load_config, patch.object(
        mock_config, "print_config"
    ) as mock_print_config, patch.object(mock_server, "start", side_effect=Exception("Start error")):

        # When / Then
        with pytest.raises(Exception, match="Start error"):
            main(mock_config, mock_server)
        mock_load_config.assert_called_once()
        mock_print_config.assert_called_once()
