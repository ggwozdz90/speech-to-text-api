from unittest.mock import Mock

import pytest

from core.config.app_config import AppConfig
from data.workers.mbart_translation_worker import MBartTranslationWorker
from data.workers.seamless_translation_worker import SeamlessTranslationWorker
from src.data.factories.translation_worker_factory import TranslationWorkerFactory


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


def test_create_mbart(mock_config: AppConfig) -> None:
    # Given
    mock_config.translation_model_name = "facebook/mbart-large-50-many-to-many-mmt"
    mock_config.device = "cpu"
    mock_config.translation_model_download_path = "/path/to/mbart"

    factory = TranslationWorkerFactory(config=mock_config)

    # When
    worker = factory.create()

    # Then
    assert isinstance(worker, MBartTranslationWorker)
    assert worker._config.device == "cpu"
    assert worker._config.model_name == "facebook/mbart-large-50-many-to-many-mmt"
    assert worker._config.model_download_path == "/path/to/mbart"


def test_create_seamless(mock_config: AppConfig) -> None:
    # Given
    mock_config.translation_model_name = "facebook/seamless-m4t-v2-large"
    mock_config.device = "cpu"
    mock_config.translation_model_download_path = "/path/to/seamless"

    factory = TranslationWorkerFactory(config=mock_config)

    # When
    worker = factory.create()

    # Then
    assert isinstance(worker, SeamlessTranslationWorker)
    assert worker._config.device == "cpu"
    assert worker._config.model_name == "facebook/seamless-m4t-v2-large"
    assert worker._config.model_download_path == "/path/to/seamless"


def test_create_unsupported_model(mock_config: AppConfig) -> None:
    # Given
    mock_config.translation_model_name = "unsupported-model"
    factory = TranslationWorkerFactory(config=mock_config)

    # When / Then
    with pytest.raises(ValueError, match="Unsupported translation model name: unsupported-model"):
        factory.create()
