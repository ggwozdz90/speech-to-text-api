import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.health_check_router import HealthCheckRouter


@pytest.fixture
def client() -> TestClient:
    router = HealthCheckRouter()
    app = FastAPI()
    app.include_router(router.router)
    return TestClient(app)


def test_healthcheck_success(client: TestClient) -> None:
    # When
    response = client.get("/healthcheck")

    # Then
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
