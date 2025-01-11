from unittest.mock import Mock, patch

import pytest
import uvicorn
from fastapi import FastAPI

from api.server import APIServer
from core.config.app_config import AppConfig
from core.logger.logger import Logger


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def api_server(mock_config: AppConfig, mock_logger: Logger) -> APIServer:
    return APIServer(config=mock_config, logger=mock_logger)


def test_api_server_initialization(
    api_server: APIServer,
    mock_config: AppConfig,
) -> None:
    # Given / When
    app = api_server.app

    # Then
    assert isinstance(app, FastAPI)
    assert any(isinstance(middleware, type(api_server.app.user_middleware[0])) for middleware in app.user_middleware)
    assert any(getattr(route, "path", None) == "/healthcheck" for route in app.routes)


def test_api_server_start(
    api_server: APIServer,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_config.fastapi_host = "127.0.0.1"
    mock_config.fastapi_port = 8000

    with patch.object(uvicorn, "run") as mock_run:
        # When
        api_server.start()

        # Then
        mock_run.assert_called_once_with(
            api_server.app,
            host=mock_config.fastapi_host,
            port=mock_config.fastapi_port,
            server_header=False,
            log_config=None,
        )
