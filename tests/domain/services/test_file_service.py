import os
from unittest.mock import AsyncMock, Mock, mock_open, patch

import pytest
from fastapi import UploadFile

from config.app_config import AppConfig
from domain.services.file_service import FileService


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def file_service(mock_config: AppConfig) -> FileService:
    return FileService(config=mock_config)


@pytest.mark.asyncio
async def test_save_file(
    file_service: FileService,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_file.read = AsyncMock(side_effect=[b"file content", b""])
    mock_config.file_upload_path = "test_upload_path"
    expected_path = os.path.join(mock_config.file_upload_path, mock_file.filename)

    with patch("builtins.open", mock_open()) as mock_open_func:
        # When
        result = await file_service.save_file(mock_file)

        # Then
        assert result == os.path.abspath(expected_path)
        mock_open_func.assert_called_once_with(os.path.abspath(expected_path), "wb")


@pytest.mark.asyncio
async def test_save_file_invalid_path(
    file_service: FileService,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "../test_file.txt"
    mock_config.file_upload_path = "test_upload_path"

    # When / Then
    with pytest.raises(Exception, match="Invalid file name"):
        await file_service.save_file(mock_file)


def test_delete_file(
    file_service: FileService,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_config.file_upload_path = "test_upload_path"
    test_path = os.path.join(mock_config.file_upload_path, "test_file.txt")

    with patch("os.remove") as mock_remove:
        # When
        file_service.delete_file(test_path)

        # Then
        mock_remove.assert_called_once_with(os.path.abspath(test_path))


def test_delete_file_invalid_path(
    file_service: FileService,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_config.file_upload_path = "test_upload_path"
    test_path = "../test_file.txt"

    # When / Then
    with pytest.raises(Exception, match="Invalid file path"):
        file_service.delete_file(test_path)
