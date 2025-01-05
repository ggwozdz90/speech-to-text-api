import time
import uuid
from typing import Any, Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.logger.logger import Logger


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Any,
        logger: Logger,
    ) -> None:
        super().__init__(app)
        self.logger = logger

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = str(uuid.uuid4())
        self.logger.info(f"Request {request_id} started: {request.method} {request.url}")
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        self.logger.info(
            f"Request {request_id} completed: {request.method} {request.url} processed in {process_time:.4f} seconds.",
        )
        return response
