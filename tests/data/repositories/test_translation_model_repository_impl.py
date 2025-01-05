from unittest.mock import Mock, patch

import pytest

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from core.timer.timer import Timer, TimerFactory
from data.factories.translation_worker_factory import TranslationWorkerFactory
from data.repositories.translation_model_repository_impl import (
    TranslationModelRepositoryImpl,
)
from domain.repositories.directory_repository import DirectoryRepository


@pytest.fixture
def mock_config() -> AppConfig:
    config = Mock(AppConfig)
    config.translation_model_download_path = "/models"
    config.device = "cpu"
    config.translation_model_name = "openai/translation"
    config.translation_model_type = "base"
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
    return Mock()


@pytest.fixture
def mock_worker_factory(mock_worker: Mock) -> Mock:
    factory = Mock(spec=TranslationWorkerFactory)
    factory.create.return_value = mock_worker
    return factory


@pytest.fixture
def translation_model_repository_impl(
    mock_config: Mock,
    mock_directory_repository: Mock,
    mock_timer_factory: Mock,
    mock_logger: Mock,
    mock_worker_factory: Mock,
) -> TranslationModelRepositoryImpl:
    with patch.object(TranslationModelRepositoryImpl, "_instance", None):
        return TranslationModelRepositoryImpl(
            config=mock_config,
            directory_repository=mock_directory_repository,
            timer_factory=mock_timer_factory,
            logger=mock_logger,
            worker_factory=mock_worker_factory,
        )


def test_translate_success(
    translation_model_repository_impl: TranslationModelRepositoryImpl,
    mock_worker: Mock,
    mock_timer: Mock,
) -> None:
    # Given
    mock_worker.is_alive.return_value = False
    mock_worker.translate.return_value = "translated text"

    # When
    result = translation_model_repository_impl.translate("text to translate", "en", "fr")

    # Then
    assert result == "translated text"
    mock_worker.start.assert_called_once()
    mock_worker.translate.assert_called_once_with("text to translate", "en", "fr")
    mock_timer.start.assert_called_once_with(60, translation_model_repository_impl._check_idle_timeout)


def test_check_idle_timeout_stops_worker(
    translation_model_repository_impl: TranslationModelRepositoryImpl,
    mock_worker: Mock,
    mock_timer: Mock,
    mock_logger: Mock,
) -> None:
    # Given
    mock_worker.is_alive.return_value = True
    mock_worker.is_processing.return_value = False

    # When
    translation_model_repository_impl._check_idle_timeout()

    # Then
    mock_worker.stop.assert_called_once()
    mock_timer.cancel.assert_called_once()
    mock_logger.debug.assert_any_call("Checking translation model idle timeout")
    mock_logger.info.assert_any_call("Translation model stopped due to idle timeout")
