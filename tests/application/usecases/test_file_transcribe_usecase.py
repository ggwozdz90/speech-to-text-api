from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from application.usecases.file_transcribe_usecase import FileTranscribeUseCase
from config.app_config import AppConfig
from domain.services.file_service import FileService
from domain.services.transcription_service import TranscriptionService


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_file_service() -> FileService:
    return Mock(FileService)


@pytest.fixture
def mock_transcription_service() -> TranscriptionService:
    return Mock(TranscriptionService)


@pytest.fixture
def use_case(
    mock_config: AppConfig,
    mock_file_service: FileService,
    mock_transcription_service: TranscriptionService,
) -> FileTranscribeUseCase:
    return FileTranscribeUseCase(
        config=mock_config,
        file_service=mock_file_service,
        transcription_service=mock_transcription_service,
    )


@pytest.mark.asyncio
async def test_execute_success(
    use_case: FileTranscribeUseCase,
    mock_file_service: FileService,
    mock_transcription_service: TranscriptionService,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file_service.save_file = AsyncMock(return_value="test_path")
    mock_transcription_service.transcribe.return_value = "transcription_result"
    mock_config.delete_files_after_transcription = False

    # When
    result = await use_case.execute(mock_file, "en")

    # Then
    mock_file_service.save_file.assert_awaited_once_with(mock_file)
    mock_transcription_service.transcribe.assert_called_once_with("test_path", "en")
    assert result == "transcription_result"
    mock_file_service.delete_file.assert_not_called()


@pytest.mark.asyncio
async def test_execute_delete_file_after_transcription(
    use_case: FileTranscribeUseCase,
    mock_file_service: FileService,
    mock_transcription_service: TranscriptionService,
    mock_config: AppConfig,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file_service.save_file = AsyncMock(return_value="test_path")
    mock_transcription_service.transcribe.return_value = "transcription_result"
    mock_config.delete_files_after_transcription = True

    # When
    result = await use_case.execute(mock_file, "en")

    # Then
    mock_file_service.save_file.assert_awaited_once_with(mock_file)
    mock_transcription_service.transcribe.assert_called_once_with("test_path", "en")
    mock_file_service.delete_file.assert_called_once_with("test_path")
    assert result == "transcription_result"


@pytest.mark.asyncio
async def test_execute_save_file_exception(
    use_case: FileTranscribeUseCase,
    mock_file_service: FileService,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file_service.save_file = AsyncMock(side_effect=Exception("Save file error"))

    # When / Then
    with pytest.raises(Exception, match="Save file error"):
        await use_case.execute(mock_file, "en")
    mock_file_service.save_file.assert_awaited_once_with(mock_file)


@pytest.mark.asyncio
async def test_execute_transcription_exception(
    use_case: FileTranscribeUseCase,
    mock_file_service: FileService,
    mock_transcription_service: TranscriptionService,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file_service.save_file = AsyncMock(return_value="test_path")
    mock_transcription_service.transcribe = Mock(side_effect=Exception("Transcription error"))

    # When / Then
    with pytest.raises(Exception, match="Transcription error"):
        await use_case.execute(mock_file, "en")
    mock_file_service.save_file.assert_awaited_once_with(mock_file)
    mock_transcription_service.transcribe.assert_called_once_with("test_path", "en")
