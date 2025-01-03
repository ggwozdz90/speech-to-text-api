import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.dtos.error_response_dto import ErrorResponseDto
from core.logger.logger import Logger


class GlobalExceptionHandler:
    def __init__(self, app: FastAPI, logger: Logger):
        self.app = app
        self.logger = logger
        self.register_handlers()

    def register_handlers(self) -> None:
        @self.app.exception_handler(Exception)
        async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
            content = ErrorResponseDto(
                status_code=500,
                message=str(exc),
                details={"error_type": exc.__class__.__name__},
                trace=traceback.format_exc(),
            ).model_dump(exclude_none=True)

            self.logger.error(f"ErrorResponseDto: {str(content)}")

            return JSONResponse(
                status_code=500,
                content=content,
            )
