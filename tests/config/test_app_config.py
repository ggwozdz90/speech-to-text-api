import os
from unittest.mock import patch

import pytest

from src.config.app_config import AppConfig


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
            "WHISPER_MODEL_NAME": "base",
            "WHISPER_MODEL_DOWNLOAD_PATH": "model_path",
        },
    ):
        # When
        app_config.load_config()

        # Then
        assert app_config.file_upload_path == "test_path"
        assert app_config.delete_files_after_transcription is True
        assert app_config.fastapi_host == "localhost"
        assert app_config.fastapi_port == 8000
        assert app_config.whisper_model_name == "base"
        assert app_config.whisper_model_download_path == "model_path"


def test_print_config(
    app_config: AppConfig,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Given
    app_config.file_upload_path = "test_path"
    app_config.delete_files_after_transcription = True
    app_config.fastapi_host = "localhost"
    app_config.fastapi_port = 8000
    app_config.whisper_model_name = "base"
    app_config.whisper_model_download_path = "model_path"

    # When
    app_config.print_config()
    captured = capsys.readouterr()

    # Then
    assert "### APP CONFIG START ###" in captured.out
    assert "FILE_UPLOAD_PATH: test_path" in captured.out
    assert "DELETE_FILES_AFTER_TRANSCRIPTION: True" in captured.out
    assert "FASTAPI_HOST: localhost" in captured.out
    assert "FASTAPI_PORT: 8000" in captured.out
    assert "WHISPER_MODEL_NAME: base" in captured.out
    assert "WHISPER_MODEL_DOWNLOAD_PATH: model_path" in captured.out
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
        assert app_config.whisper_model_name == "turbo"
        assert app_config.whisper_model_download_path == "downloaded_whisper_models"


def test_load_config_invalid_port(app_config: AppConfig) -> None:
    # Given
    with patch.dict(os.environ, {"FASTAPI_PORT": "invalid_port"}):
        # When
        app_config.load_config()

        # Then
        assert app_config.fastapi_port == 8000  # Default value
