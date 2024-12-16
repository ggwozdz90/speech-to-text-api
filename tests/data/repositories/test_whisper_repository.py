from unittest.mock import Mock, patch

import pytest

from config.app_config import AppConfig
from data.repositories.whisper_repository import WhisperRepository


@pytest.fixture
def mock_config() -> AppConfig:
    mock = Mock(AppConfig)
    mock.whisper_model_name = "base"
    mock.whisper_model_download_path = "model_path"
    return mock


@pytest.fixture
def whisper_repository(mock_config: AppConfig) -> WhisperRepository:
    with patch("whisper.load_model", return_value=Mock()):
        return WhisperRepository(config=mock_config)


def test_whisper_repository_initialization(mock_config: AppConfig) -> None:
    # Given
    with patch("whisper.load_model") as mock_load_model:
        # When
        repository = WhisperRepository(config=mock_config)

        # Then
        mock_load_model.assert_called_once_with("base", download_root="model_path")
        assert repository.model is not None


def test_transcribe(whisper_repository: WhisperRepository) -> None:
    # Given
    file_path = "test_path"
    language = "en"
    whisper_repository.model = Mock()
    whisper_repository.model.transcribe.return_value = {"text": "transcription_result"}

    # When
    result = whisper_repository.transcribe(file_path, language)

    # Then
    whisper_repository.model.transcribe.assert_called_once_with(file_path, language=language)
    assert result == {"text": "transcription_result"}
