from unittest.mock import Mock, patch

import pytest

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.timer.timer import Timer, TimerFactory
from data.repositories.speach_to_text_repository_impl import SpeachToTextRepositoryImpl
from data.workers.whisper_worker import WhisperConfig, WhisperWorker
from domain.repositories.directory_repository import DirectoryRepository


@pytest.fixture
def mock_config() -> AppConfig:
    config = Mock(AppConfig)
    config.speach_to_text_model_download_path = "/models"
    config.device = "cpu"
    config.speach_to_text_model_name = "openai/whisper"
    config.speach_to_text_model_type = "base"
    config.model_idle_timeout = 60
    return config


@pytest.fixture
def mock_directory_repository() -> Mock:
    return Mock(spec=DirectoryRepository)


@pytest.fixture
def mock_timer() -> Mock:
    return Mock(spec=Timer)


@pytest.fixture
def mock_timer_factory(mock_timer: Mock) -> Mock:
    factory = Mock(spec=TimerFactory)
    factory.create.return_value = mock_timer
    return factory


@pytest.fixture
def mock_logger() -> Mock:
    return Mock(spec=Logger)


@pytest.fixture
def mock_worker() -> Mock:
    return Mock(spec=WhisperWorker)


@pytest.fixture
def speach_to_text_repository_impl(
    mock_config: Mock,
    mock_directory_repository: Mock,
    mock_timer_factory: Mock,
    mock_logger: Mock,
    mock_worker: Mock,
) -> SpeachToTextRepositoryImpl:
    with patch.object(SpeachToTextRepositoryImpl, "_instance", None):
        return SpeachToTextRepositoryImpl(
            config=mock_config,
            directory_repository=mock_directory_repository,
            timer_factory=mock_timer_factory,
            logger=mock_logger,
            worker=mock_worker,
        )


def test_transcribe_success(
    speach_to_text_repository_impl: SpeachToTextRepositoryImpl, mock_worker: Mock, mock_timer: Mock
) -> None:
    # Given
    mock_worker.is_alive.return_value = False
    mock_worker.transcribe.return_value = {"text": "transcribed text"}

    # When
    result = speach_to_text_repository_impl.transcribe("path/to/file", "en")

    # Then
    assert result == {"text": "transcribed text"}
    mock_worker.start.assert_called_once_with(
        WhisperConfig(
            device="cpu",
            model_type="base",
            model_download_path="/models",
        )
    )
    mock_worker.transcribe.assert_called_once_with("path/to/file", "en")
    mock_timer.start.assert_called_once_with(60, speach_to_text_repository_impl._check_idle_timeout)


def test_check_idle_timeout_stops_worker(
    speach_to_text_repository_impl: SpeachToTextRepositoryImpl, mock_worker: Mock, mock_timer: Mock, mock_logger: Mock
) -> None:
    # Given
    mock_worker.is_alive.return_value = True
    mock_worker.is_processing.return_value = False

    # When
    speach_to_text_repository_impl._check_idle_timeout()

    # Then
    mock_worker.stop.assert_called_once()
    mock_timer.cancel.assert_called_once()
    mock_logger.info.assert_any_call("Checking speach to text model idle timeout")
    mock_logger.info.assert_any_call("Speach to text model stopped due to idle timeout")
