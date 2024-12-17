from unittest.mock import Mock, patch

import pytest

from config.app_config import AppConfig
from data.repositories.whisper_repository_impl import WhisperRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository


@pytest.fixture
def mock_config() -> AppConfig:
    mock = Mock(AppConfig)
    mock.whisper_model_name = "base"
    mock.whisper_model_download_path = "model_path"
    return mock


@pytest.fixture
def mock_directory_repository() -> DirectoryRepository:
    return Mock(DirectoryRepository)


@pytest.fixture
def whisper_repository(mock_config: AppConfig, mock_directory_repository: DirectoryRepository) -> WhisperRepositoryImpl:
    with patch("whisper.load_model", return_value=Mock()):
        return WhisperRepositoryImpl(config=mock_config, directory_repository=mock_directory_repository)


def test_whisper_repository_initialization(
    mock_config: AppConfig,
    mock_directory_repository: DirectoryRepository,
) -> None:
    # Given
    with patch("whisper.load_model") as mock_load_model:
        # When
        repository = WhisperRepositoryImpl(config=mock_config, directory_repository=mock_directory_repository)

        # Then
        mock_load_model.assert_called_once_with("base", download_root="model_path")
        mock_directory_repository.create_directory.assert_called_once_with("model_path")
        assert repository.model is not None


def test_transcribe(whisper_repository: WhisperRepositoryImpl) -> None:
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
