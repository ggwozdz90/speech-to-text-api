import os
from unittest.mock import Mock, patch

import pytest

from core.config.app_config import AppConfig
from core.logger.logger import Logger


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def app_config() -> AppConfig:
    return AppConfig()


def test_initialize(app_config: AppConfig, mock_logger: Logger) -> None:
    # Given
    with patch.dict(
        os.environ,
        {
            "FILE_UPLOAD_PATH": "test_path",
            "DELETE_FILES_AFTER_TRANSCRIPTION": "true",
            "FASTAPI_HOST": "localhost",
            "FASTAPI_PORT": "8000",
            "SPEECH_TO_TEXT_MODEL_NAME": "openai/whisper",
            "SPEECH_TO_TEXT_MODEL_TYPE": "base",
            "SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH": "model_path",
            "TRANSLATION_MODEL_NAME": "test_translation_model",
            "TRANSLATION_MODEL_DOWNLOAD_PATH": "translation_model_path",
            "MODEL_IDLE_TIMEOUT": "150",
        },
    ):
        # When
        app_config.initialize(mock_logger)

        # Then
        assert app_config.file_upload_path == "test_path"
        assert app_config.delete_files_after_transcription is True
        assert app_config.fastapi_host == "localhost"
        assert app_config.fastapi_port == 8000
        assert app_config.speech_to_text_model_name == "openai/whisper"
        assert app_config.speech_to_text_model_type == "base"
        assert app_config.speech_to_text_model_download_path == "model_path"
        assert app_config.translation_model_name == "test_translation_model"
        assert app_config.translation_model_download_path == "translation_model_path"
        assert app_config.model_idle_timeout == 150


def test_initialize_invalid_port(app_config: AppConfig, mock_logger: Logger) -> None:
    # Given
    with patch.dict(os.environ, {"FASTAPI_PORT": "invalid_port"}):
        # When
        app_config.initialize(mock_logger)

        # Then
        assert app_config.fastapi_port == 8000  # Default value


def test_initialize_log_parameters(app_config: AppConfig, mock_logger: Logger) -> None:
    # When
    app_config.initialize(mock_logger)

    # Then
    mock_logger.info.assert_called()
    assert mock_logger.info.call_count == 3
    assert mock_logger.info.call_args_list[0][0][0] == "Initializing configuration..."
    assert mock_logger.info.call_args_list[1][0][0].startswith("Configuration loaded:")
    assert "LOG_LEVEL" in mock_logger.info.call_args_list[1][0][0]
    assert "DEVICE" in mock_logger.info.call_args_list[1][0][0]
    assert "FILE_UPLOAD_PATH" in mock_logger.info.call_args_list[1][0][0]
    assert "DELETE_FILES_AFTER_TRANSCRIPTION" in mock_logger.info.call_args_list[1][0][0]
    assert "FASTAPI_HOST" in mock_logger.info.call_args_list[1][0][0]
    assert "FASTAPI_PORT" in mock_logger.info.call_args_list[1][0][0]
    assert "SPEECH_TO_TEXT_MODEL_NAME" in mock_logger.info.call_args_list[1][0][0]
    assert "SPEECH_TO_TEXT_MODEL_TYPE" in mock_logger.info.call_args_list[1][0][0]
    assert "SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH" in mock_logger.info.call_args_list[1][0][0]
    assert "TRANSLATION_MODEL_NAME" in mock_logger.info.call_args_list[1][0][0]
    assert "TRANSLATION_MODEL_DOWNLOAD_PATH" in mock_logger.info.call_args_list[1][0][0]
    assert "MODEL_IDLE_TIMEOUT" in mock_logger.info.call_args_list[1][0][0]
    assert mock_logger.info.call_args_list[2][0][0] == "Configuration initialized successfully."
