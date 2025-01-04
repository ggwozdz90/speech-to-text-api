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
        @self.app.exception_handler(ValueError)
        async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
            content = ErrorResponseDto(
                status_code=422,
                message="Value error",
                details={"error_type": exc.__class__.__name__, "error_message": str(exc)},
                trace=traceback.format_exception(exc),
            ).model_dump(exclude_none=True)

            self.logger.error(f"ValueError occurred: {str(content)}")

            return JSONResponse(
                status_code=422,
                content=content,
            )

        @self.app.exception_handler(Exception)
        async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
            content = ErrorResponseDto(
                status_code=500,
                message="Internal server error",
                details={"error_type": exc.__class__.__name__, "error_message": str(exc)},
                trace=traceback.format_exception(exc),
            ).model_dump(exclude_none=True)

            self.logger.error(f"Exception occurred: {str(content)}")

            return JSONResponse(
                status_code=500,
                content=content,
            )
