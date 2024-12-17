import os
from unittest.mock import AsyncMock, Mock, mock_open, patch

import pytest
from fastapi import UploadFile

from config.app_config import AppConfig
from data.repositories.file_repository_impl import FileRepositoryImpl
from domain.repositories.directory_repository import DirectoryRepository


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_directory_repository() -> DirectoryRepository:
    return Mock(DirectoryRepository)


@pytest.fixture
def file_repository(mock_config: AppConfig, mock_directory_repository: DirectoryRepository) -> FileRepositoryImpl:
    return FileRepositoryImpl(config=mock_config, directory_repository=mock_directory_repository)


@pytest.mark.asyncio
async def test_save_file(
    file_repository: FileRepositoryImpl,
    mock_config: AppConfig,
    mock_directory_repository: DirectoryRepository,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_file.read = AsyncMock(side_effect=[b"file content", b""])
    mock_config.file_upload_path = "test_upload_path"
    expected_path = os.path.join(mock_config.file_upload_path, mock_file.filename)

    with patch("builtins.open", mock_open()) as mock_open_func:
        # When
        result = await file_repository.save_file(mock_file)

        # Then
        assert result == os.path.abspath(expected_path)
        mock_open_func.assert_called_once_with(os.path.abspath(expected_path), "wb")
        mock_directory_repository.create_directory.assert_called_once_with(mock_config.file_upload_path)


@pytest.mark.asyncio
async def test_save_file_invalid_path(
    file_repository: FileRepositoryImpl,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "../test_file.txt"
    mock_config.file_upload_path = "test_upload_path"

    # When / Then
    with pytest.raises(Exception, match="Invalid file name"):
        await file_repository.save_file(mock_file)


def test_delete_file(
    file_repository: FileRepositoryImpl,
    mock_config: AppConfig,
    mock_directory_repository: DirectoryRepository,
) -> None:
    # Given
    mock_config.file_upload_path = "test_upload_path"
    test_path = os.path.join(mock_config.file_upload_path, "test_file.txt")

    with patch("os.remove") as mock_remove:
        # When
        file_repository.delete_file(test_path)

        # Then
        mock_remove.assert_called_once_with(os.path.abspath(test_path))
        mock_directory_repository.create_directory.assert_called_once_with(mock_config.file_upload_path)


def test_delete_file_invalid_path(
    file_repository: FileRepositoryImpl,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_config.file_upload_path = "test_upload_path"
    test_path = "../test_file.txt"

    # When / Then
    with pytest.raises(Exception, match="Invalid file path"):
        file_repository.delete_file(test_path)
