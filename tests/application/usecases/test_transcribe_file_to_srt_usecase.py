from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from config.app_config import AppConfig
from domain.repositories.file_repository import FileRepository
from domain.services.subtitle_service import SubtitleService
from domain.services.transcription_service import TranscriptionService
from src.application.usecases.transcribe_file_to_srt_usecase import (
    TranscribeFileToSrtUseCase,
)


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_file_repository() -> FileRepository:
    return Mock(FileRepository)


@pytest.fixture
def mock_transcription_service() -> TranscriptionService:
    return Mock(TranscriptionService)


@pytest.fixture
def mock_subtitle_service() -> Mock:
    return Mock(SubtitleService)


@pytest.fixture
def usecase(
    mock_config: Mock,
    mock_transcription_service: Mock,
    mock_file_repository: Mock,
    mock_subtitle_service: Mock,
) -> TranscribeFileToSrtUseCase:
    return TranscribeFileToSrtUseCase(
        config=mock_config,
        transcription_service=mock_transcription_service,
        file_repository=mock_file_repository,
        subtitle_service=mock_subtitle_service,
    )


@pytest.mark.asyncio
async def test_execute_success(
    usecase: TranscribeFileToSrtUseCase,
    mock_file_repository: Mock,
    mock_transcription_service: Mock,
    mock_subtitle_service: Mock,
    mock_config: AppConfig,
) -> None:
    # Given
    file = Mock(UploadFile)
    language = "en"
    file_path = "path/to/file"
    transcription_result = "transcription result"
    srt_result = "srt result"

    mock_file_repository.save_file = AsyncMock(return_value=file_path)
    mock_transcription_service.transcribe.return_value = transcription_result
    mock_subtitle_service.convert_to_srt.return_value = srt_result
    mock_config.delete_files_after_transcription = True

    # When
    result = await usecase.execute(file, language)

    # Then
    assert result == srt_result
    mock_file_repository.save_file.assert_awaited_once_with(file)
    mock_transcription_service.transcribe.assert_called_once_with(file_path, language)
    mock_subtitle_service.convert_to_srt.assert_called_once_with(transcription_result)
    mock_file_repository.delete_file.assert_called_once_with(file_path)


@pytest.mark.asyncio
async def test_execute_no_delete(
    usecase: TranscribeFileToSrtUseCase,
    mock_file_repository: Mock,
    mock_transcription_service: Mock,
    mock_subtitle_service: Mock,
    mock_config: Mock,
) -> None:
    # Given
    mock_config.delete_files_after_transcription = False
    file = Mock(UploadFile)
    language = "en"
    file_path = "path/to/file"
    transcription_result = "transcription result"
    srt_result = "srt result"

    mock_file_repository.save_file = AsyncMock(return_value=file_path)
    mock_transcription_service.transcribe.return_value = transcription_result
    mock_subtitle_service.convert_to_srt.return_value = srt_result

    # When
    result = await usecase.execute(file, language)

    # Then
    assert result == srt_result
    mock_file_repository.save_file.assert_awaited_once_with(file)
    mock_transcription_service.transcribe.assert_called_once_with(file_path, language)
    mock_subtitle_service.convert_to_srt.assert_called_once_with(transcription_result)
    mock_file_repository.delete_file.assert_not_called()


@pytest.mark.asyncio
async def test_execute_transcription_failure(
    usecase: TranscribeFileToSrtUseCase, mock_file_repository: Mock, mock_transcription_service: Mock
) -> None:
    # Given
    file = Mock(UploadFile)
    language = "en"
    file_path = "path/to/file"

    mock_file_repository.save_file = AsyncMock(return_value=file_path)
    mock_transcription_service.transcribe.side_effect = Exception("Transcription failed")

    # When / Then
    with pytest.raises(Exception, match="Transcription failed"):
        await usecase.execute(file, language)
    mock_file_repository.save_file.assert_awaited_once_with(file)
    mock_transcription_service.transcribe.assert_called_once_with(file_path, language)
    mock_file_repository.delete_file.assert_not_called()
