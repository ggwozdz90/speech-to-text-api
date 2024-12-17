from unittest.mock import Mock

import pytest

from config.app_config import AppConfig
from domain.models.transcription_result_model import TranscriptionResultModel
from domain.repositories.whisper_repository import WhisperRepository
from domain.services.transcription_service import TranscriptionService


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_whisper_repository() -> WhisperRepository:
    return Mock(WhisperRepository)


@pytest.fixture
def transcription_service(
    mock_config: AppConfig,
    mock_whisper_repository: WhisperRepository,
) -> TranscriptionService:
    return TranscriptionService(config=mock_config, whisper_repository=mock_whisper_repository)


def test_transcribe(
    transcription_service: TranscriptionService,
    mock_whisper_repository: WhisperRepository,
) -> None:
    # Given
    file_path = "test_path"
    language = "en"
    mock_whisper_repository.transcribe.return_value = {"text": "transcription_result", "segments": []}

    # When
    result = transcription_service.transcribe(file_path, language)

    # Then
    mock_whisper_repository.transcribe.assert_called_once_with(file_path, language=language)
    assert result == TranscriptionResultModel(text="transcription_result", segments=[])


def test_transcribe_exception(
    transcription_service: TranscriptionService,
    mock_whisper_repository: WhisperRepository,
) -> None:
    # Given
    file_path = "test_path"
    language = "en"
    mock_whisper_repository.transcribe.side_effect = Exception("Transcription error")

    # When / Then
    with pytest.raises(Exception, match="Transcription error"):
        transcription_service.transcribe(file_path, language)
    mock_whisper_repository.transcribe.assert_called_once_with(file_path, language=language)
