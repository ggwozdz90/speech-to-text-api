import os
from unittest.mock import patch

import pytest

from core.config.app_config import AppConfig


@pytest.fixture
def app_config() -> AppConfig:
    return AppConfig()


def test_load_config(app_config: AppConfig) -> None:
    # Given
    with patch.dict(
        os.environ,
        {
            "FILE_UPLOAD_PATH": "test_path",
            "DELETE_FILES_AFTER_TRANSCRIPTION": "true",
            "FASTAPI_HOST": "localhost",
            "FASTAPI_PORT": "8000",
            "SPEACH_TO_TEXT_MODEL_NAME": "openai/whisper",
            "SPEACH_TO_TEXT_MODEL_TYPE": "base",
            "SPEACH_TO_TEXT_MODEL_DOWNLOAD_PATH": "model_path",
            "TRANSLATION_MODEL_NAME": "test_translation_model",
            "TRANSLATION_MODEL_DOWNLOAD_PATH": "translation_model_path",
            "MODEL_IDLE_TIMEOUT": "150",
        },
    ):
        # When
        app_config.load_config()

        # Then
        assert app_config.file_upload_path == "test_path"
        assert app_config.delete_files_after_transcription is True
        assert app_config.fastapi_host == "localhost"
        assert app_config.fastapi_port == 8000
        assert app_config.speach_to_text_model_name == "openai/whisper"
        assert app_config.speach_to_text_model_type == "base"
        assert app_config.speach_to_text_model_download_path == "model_path"
        assert app_config.translation_model_name == "test_translation_model"
        assert app_config.translation_model_download_path == "translation_model_path"
        assert app_config.model_idle_timeout == 150


def test_print_config(
    app_config: AppConfig,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Given
    app_config.file_upload_path = "test_path"
    app_config.delete_files_after_transcription = True
    app_config.fastapi_host = "localhost"
    app_config.fastapi_port = 8000
    app_config.speach_to_text_model_name = "openai/whisper"
    app_config.speach_to_text_model_type = "base"
    app_config.speach_to_text_model_download_path = "model_path"
    app_config.translation_model_name = "test_translation_model"
    app_config.translation_model_download_path = "translation_model_path"
    app_config.model_idle_timeout = 150

    # When
    app_config.print_config()
    captured = capsys.readouterr()

    # Then
    assert "### APP CONFIG START ###" in captured.out
    assert "FILE_UPLOAD_PATH: test_path" in captured.out
    assert "DELETE_FILES_AFTER_TRANSCRIPTION: True" in captured.out
    assert "FASTAPI_HOST: localhost" in captured.out
    assert "FASTAPI_PORT: 8000" in captured.out
    assert "SPEACH_TO_TEXT_MODEL_NAME: openai/whisper" in captured.out
    assert "SPEACH_TO_TEXT_MODEL_TYPE: base" in captured.out
    assert "SPEACH_TO_TEXT_MODEL_DOWNLOAD_PATH: model_path" in captured.out
    assert "TRANSLATION_MODEL_NAME: test_translation_model" in captured.out
    assert "TRANSLATION_MODEL_DOWNLOAD_PATH: translation_model_path" in captured.out
    assert "MODEL_IDLE_TIMEOUT: 150" in captured.out
    assert "### APP CONFIG END ###" in captured.out


def test_load_config_missing_env_vars(app_config: AppConfig) -> None:
    # Given
    with patch.dict(os.environ, {}, clear=True):
        # When
        app_config.load_config()

        # Then
        assert app_config.file_upload_path == "uploaded_files"
        assert app_config.delete_files_after_transcription is True
        assert app_config.fastapi_host == "127.0.0.1"
        assert app_config.fastapi_port == 8000
        assert app_config.speach_to_text_model_name == "openai/whisper"
        assert app_config.speach_to_text_model_type == "turbo"
        assert app_config.speach_to_text_model_download_path == "downloaded_speach_to_text_models"
        assert app_config.translation_model_name == "facebook/mbart-large-50-many-to-many-mmt"
        assert app_config.translation_model_download_path == "downloaded_translation_models"
        assert app_config.model_idle_timeout == 60


def test_load_config_invalid_port(app_config: AppConfig) -> None:
    # Given
    with patch.dict(os.environ, {"FASTAPI_PORT": "invalid_port"}):
        # When
        app_config.load_config()

        # Then
        assert app_config.fastapi_port == 8000  # Default value
