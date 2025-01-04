from unittest.mock import Mock

import pytest

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.workers.whisper_speach_to_text_worker import WhisperSpeachToTextWorker
from src.data.factories.speach_to_text_worker_factory import SpeachToTextWorkerFactory


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


def test_create_worker_whisper(mock_config: AppConfig, mock_logger: Logger) -> None:
    # Given
    mock_config.speach_to_text_model_name = "openai/whisper"
    mock_config.device = "cpu"
    mock_config.speach_to_text_model_type = "base"
    mock_config.speach_to_text_model_download_path = "/path/to/whisper"
    mock_config.log_level = "INFO"

    factory = SpeachToTextWorkerFactory(config=mock_config, logger=mock_logger)

    # When
    worker = factory.create()

    # Then
    assert isinstance(worker, WhisperSpeachToTextWorker)
    assert worker._config.device == "cpu"
    assert worker._config.model_type == "base"
    assert worker._config.model_download_path == "/path/to/whisper"


def test_create_worker_unsupported_model(mock_config: AppConfig, mock_logger: Logger) -> None:
    # Given
    mock_config.speach_to_text_model_name = "unsupported-model"
    factory = SpeachToTextWorkerFactory(config=mock_config, logger=mock_logger)

    # When / Then
    with pytest.raises(ValueError, match="Unsupported speach to text model name: unsupported-model"):
        factory.create()
