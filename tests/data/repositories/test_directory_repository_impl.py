from unittest.mock import Mock, patch

import pytest

from core.logger.logger import Logger
from src.data.repositories.directory_repository_impl import DirectoryRepositoryImpl


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def directory_repository(mock_logger: Logger) -> DirectoryRepositoryImpl:
    return DirectoryRepositoryImpl(logger=mock_logger)


def test_create_directory_success(directory_repository: DirectoryRepositoryImpl) -> None:
    # Given
    path = "test_path"
    with patch("os.path.exists", return_value=False) as mock_exists, patch("os.makedirs") as mock_makedirs:
        # When
        directory_repository.create_directory(path)

        # Then
        mock_exists.assert_called_once_with(path)
        mock_makedirs.assert_called_once_with(path)


def test_create_directory_already_exists(directory_repository: DirectoryRepositoryImpl) -> None:
    # Given
    path = "test_path"
    with patch("os.path.exists", return_value=True) as mock_exists, patch("os.makedirs") as mock_makedirs:
        # When
        directory_repository.create_directory(path)

        # Then
        mock_exists.assert_called_once_with(path)
        mock_makedirs.assert_not_called()
