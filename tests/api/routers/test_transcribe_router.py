from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.transcribe_router import TranscribeRouter
from application.usecases.transcribe_file_to_srt_usecase import (
    TranscribeFileToSrtUseCase,
)
from application.usecases.transcribe_file_to_text_usecase import (
    TranscribeFileToTextUseCase,
)


@pytest.fixture
def mock_transcribe_file_to_text_usecase() -> TranscribeFileToTextUseCase:
    return Mock(TranscribeFileToTextUseCase)


@pytest.fixture
def mock_transcribe_file_to_srt_usecase() -> TranscribeFileToSrtUseCase:
    return Mock(TranscribeFileToSrtUseCase)


@pytest.fixture
def client(
    mock_transcribe_file_to_text_usecase: TranscribeFileToTextUseCase,
    mock_transcribe_file_to_srt_usecase: TranscribeFileToSrtUseCase,
) -> TestClient:
    router = TranscribeRouter()
    app = FastAPI()
    app.include_router(router.router)
    app.dependency_overrides[TranscribeFileToTextUseCase] = lambda: mock_transcribe_file_to_text_usecase
    app.dependency_overrides[TranscribeFileToSrtUseCase] = lambda: mock_transcribe_file_to_srt_usecase
    return TestClient(app)


def test_transcribe_success(
    client: TestClient,
    mock_transcribe_file_to_text_usecase: TranscribeFileToTextUseCase,
) -> None:
    # Given
    mock_transcribe_file_to_text_usecase.execute = AsyncMock(return_value="transcription_result")

    # When
    response = client.post(
        "/transcribe",
        params={
            "source_language": "en_US",
            "target_language": "pl_PL",
        },
        files={"file": ("test_file.txt", b"file content")},
    )

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "filename": "test_file.txt",
        "content": "transcription_result",
    }
    mock_transcribe_file_to_text_usecase.execute.assert_awaited_once()


def test_transcribe_failure(
    client: TestClient,
    mock_transcribe_file_to_text_usecase: TranscribeFileToTextUseCase,
) -> None:
    # Given
    mock_transcribe_file_to_text_usecase.execute = AsyncMock(side_effect=Exception("Transcription error"))

    # When
    response = client.post(
        "/transcribe",
        params={"source_language": "en_US"},
        files={"file": ("test_file.txt", b"file content")},
    )

    # Then
    assert response.status_code == 500
    assert response.json() == {"detail": "Transcription error"}
    mock_transcribe_file_to_text_usecase.execute.assert_awaited_once()


def test_transcribe_missing_file(client: TestClient) -> None:
    # When
    response = client.post("/transcribe")

    # Then
    assert response.status_code == 422  # Unprocessable Entity


def test_transcribe_missing_source_language(client: TestClient) -> None:
    # When
    response = client.post(
        "/transcribe",
        files={"file": ("test_file.txt", b"file content")},
    )

    # Then
    assert response.status_code == 422  # Unprocessable Entity


def test_transcribe_srt_success(
    client: TestClient,
    mock_transcribe_file_to_srt_usecase: TranscribeFileToSrtUseCase,
) -> None:
    # Given
    mock_transcribe_file_to_srt_usecase.execute = AsyncMock(return_value="transcription_result")

    # When
    response = client.post(
        "/transcribe/srt",
        params={
            "source_language": "en_US",
            "target_language": "pl_PL",
        },
        files={"file": ("test_file.txt", b"file content")},
    )

    # Then
    assert response.status_code == 200
    assert response.text == "transcription_result"


def test_transcribe_srt_failure(
    client: TestClient,
    mock_transcribe_file_to_srt_usecase: TranscribeFileToSrtUseCase,
) -> None:
    # Given
    mock_transcribe_file_to_srt_usecase.execute = AsyncMock(side_effect=Exception("Transcription error"))

    # When
    response = client.post(
        "/transcribe/srt",
        params={"source_language": "en_US"},
        files={"file": ("test_file.txt", b"file content")},
    )

    # Then
    assert response.status_code == 500
    assert response.json() == {"detail": "Transcription error"}
    mock_transcribe_file_to_srt_usecase.execute.assert_awaited_once()


def test_transcribe_srt_missing_file(client: TestClient) -> None:
    # When
    response = client.post(
        "/transcribe/srt",
        params={"source_language": "en_US"},
    )

    # Then
    assert response.status_code == 422  # Unprocessable Entity


def test_transcribe_srt_missing_source_language(client: TestClient) -> None:
    # When
    response = client.post(
        "/transcribe/srt",
        files={"file": ("test_file.txt", b"file content")},
    )

    # Then
    assert response.status_code == 422  # Unprocessable Entity
