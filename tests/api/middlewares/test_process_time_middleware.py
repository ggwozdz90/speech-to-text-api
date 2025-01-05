from unittest.mock import AsyncMock, Mock, patch

import pytest
from starlette.requests import Request
from starlette.responses import Response

from api.middlewares.process_time_middleware import ProcessTimeMiddleware
from core.logger.logger import Logger


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_call_next() -> AsyncMock:
    return AsyncMock(return_value=Response("test response"))


@pytest.mark.asyncio
async def test_process_time_middleware(mock_call_next: AsyncMock, mock_logger: Logger) -> None:
    # Given
    request = Mock(Request)
    middleware = ProcessTimeMiddleware(app=Mock(), logger=mock_logger)

    with patch("time.time", side_effect=[1.0, 2.0]):
        # When
        response = await middleware.dispatch(request, mock_call_next)

        # Then
        assert response.headers["X-Process-Time"] == "1.0"
        mock_call_next.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_process_time_middleware_exception(mock_call_next: AsyncMock, mock_logger: Logger) -> None:
    # Given
    request = Mock(Request)
    middleware = ProcessTimeMiddleware(app=Mock(), logger=mock_logger)
    mock_call_next.side_effect = Exception("test exception")

    with patch("time.time", side_effect=[1.0, 2.0]):
        # When / Then
        with pytest.raises(Exception, match="test exception"):
            await middleware.dispatch(request, mock_call_next)

        mock_call_next.assert_awaited_once_with(request)
