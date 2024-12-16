from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.transcribe_router import TranscribeRouter
from application.usecases.file_transcribe_usecase import FileTranscribeUseCase


@pytest.fixture
def mock_usecase() -> FileTranscribeUseCase:
    return Mock(FileTranscribeUseCase)


@pytest.fixture
def client(mock_usecase: FileTranscribeUseCase) -> TestClient:
    router = TranscribeRouter()
    app = FastAPI()
    app.include_router(router.router)
    app.dependency_overrides[FileTranscribeUseCase] = lambda: mock_usecase
    return TestClient(app)


def test_transcribe_success(
    client: TestClient,
    mock_usecase: FileTranscribeUseCase,
) -> None:
    # Given
    mock_usecase.execute = AsyncMock(return_value="transcription_result")

    # When
    response = client.post("/transcribe", files={"file": ("test_file.txt", b"file content")})

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "filename": "test_file.txt",
        "content": "transcription_result",
    }
    mock_usecase.execute.assert_awaited_once()


def test_transcribe_failure(
    client: TestClient,
    mock_usecase: FileTranscribeUseCase,
) -> None:
    # Given
    mock_usecase.execute = AsyncMock(side_effect=Exception("Transcription error"))

    # When
    response = client.post("/transcribe", files={"file": ("test_file.txt", b"file content")})

    # Then
    assert response.status_code == 500
    assert response.json() == {"detail": "Transcription error"}
    mock_usecase.execute.assert_awaited_once()


def test_transcribe_missing_file(client: TestClient) -> None:
    # When
    response = client.post("/transcribe")

    # Then
    assert response.status_code == 422  # Unprocessable Entity
