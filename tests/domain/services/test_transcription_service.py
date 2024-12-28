from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.repositories.file_repository import FileRepository
from domain.repositories.speach_to_text_repository import SpeachToTextRepository
from domain.services.language_mapping_service import LanguageMappingService
from domain.services.transcription_service import TranscriptionService


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    config = Mock(AppConfig)
    config.delete_files_after_transcription = True
    config.speach_to_text_model_name = "test_model"
    return config


@pytest.fixture
def mock_speach_to_text_repository() -> SpeachToTextRepository:
    return Mock(SpeachToTextRepository)


@pytest.fixture
def mock_file_repository() -> FileRepository:
    return AsyncMock(FileRepository)


@pytest.fixture
def mock_language_mapping_service() -> LanguageMappingService:
    return Mock(LanguageMappingService)


@pytest.fixture
def transcription_service(
    mock_logger: Logger,
    mock_config: AppConfig,
    mock_speach_to_text_repository: SpeachToTextRepository,
    mock_file_repository: FileRepository,
    mock_language_mapping_service: LanguageMappingService,
) -> TranscriptionService:
    return TranscriptionService(
        logger=mock_logger,
        config=mock_config,
        speach_to_text_repository=mock_speach_to_text_repository,
        file_repository=mock_file_repository,
        language_mapping_service=mock_language_mapping_service,
    )


@pytest.mark.asyncio
async def test_transcribe_success(
    transcription_service: TranscriptionService,
    mock_file_repository: FileRepository,
    mock_speach_to_text_repository: SpeachToTextRepository,
    mock_language_mapping_service: LanguageMappingService,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file"
    mock_file_repository.save_file.return_value = "test_path"
    mock_speach_to_text_repository.transcribe.return_value = {"text": "transcribed text", "segments": []}
    mock_language_mapping_service.map_language.return_value = "en"

    # When
    result = await transcription_service.transcribe(mock_file, "en")

    # Then
    assert result.text == "transcribed text"
    mock_file_repository.save_file.assert_awaited_once_with(mock_file)
    mock_speach_to_text_repository.transcribe.assert_called_once_with("test_path", language="en")
    mock_file_repository.delete_file.assert_called_once_with("test_path")


@pytest.mark.asyncio
async def test_transcribe_with_file_deletion_disabled(
    transcription_service: TranscriptionService,
    mock_file_repository: FileRepository,
    mock_speach_to_text_repository: SpeachToTextRepository,
    mock_config: AppConfig,
    mock_language_mapping_service: LanguageMappingService,
) -> None:
    # Given
    mock_config.delete_files_after_transcription = False
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file"
    mock_file_repository.save_file.return_value = "test_path"
    mock_speach_to_text_repository.transcribe.return_value = {"text": "transcribed text", "segments": []}
    mock_language_mapping_service.map_language.return_value = "en"

    # When
    result = await transcription_service.transcribe(mock_file, "en")

    # Then
    assert result.text == "transcribed text"
    mock_file_repository.save_file.assert_awaited_once_with(mock_file)
    mock_speach_to_text_repository.transcribe.assert_called_once_with("test_path", language="en")
    mock_file_repository.delete_file.assert_not_called()


@pytest.mark.asyncio
async def test_transcribe_failure(
    transcription_service: TranscriptionService,
    mock_file_repository: FileRepository,
    mock_speach_to_text_repository: SpeachToTextRepository,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file"
    mock_file_repository.save_file.side_effect = Exception("Save failed")

    # When / Then
    with pytest.raises(Exception, match="Save failed"):
        await transcription_service.transcribe(mock_file, "en")
    mock_file_repository.save_file.assert_awaited_once_with(mock_file)
    mock_speach_to_text_repository.transcribe.assert_not_called()
    mock_file_repository.delete_file.assert_not_called()
