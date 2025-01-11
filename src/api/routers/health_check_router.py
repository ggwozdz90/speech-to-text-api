from fastapi import APIRouter

from api.dtos.health_check_result_dto import HealthCheckResultDto


class HealthCheckRouter:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.get("/healthcheck")(self.healthcheck)

    async def healthcheck(self) -> HealthCheckResultDto:
        return HealthCheckResultDto(status="OK")
