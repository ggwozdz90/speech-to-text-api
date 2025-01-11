from pydantic import BaseModel


class HealthCheckResultDto(BaseModel):
    status: str
