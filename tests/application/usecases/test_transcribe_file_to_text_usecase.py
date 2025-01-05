from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from application.usecases.transcribe_file_to_text_usecase import (
    TranscribeFileToTextUseCase,
)
from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.models.transcription_result_model import TranscriptionResultModel
from domain.repositories.file_repository import FileRepository
from domain.services.transcription_service import TranscriptionService
from domain.services.translation_service import TranslationService


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


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
def mock_translation_service() -> TranslationService:
    return Mock(TranslationService)


@pytest.fixture
def use_case(
    mock_config: AppConfig,
    mock_logger: Logger,
    mock_transcription_service: TranscriptionService,
    mock_translation_service: TranslationService,
) -> TranscribeFileToTextUseCase:
    return TranscribeFileToTextUseCase(
        config=mock_config,
        logger=mock_logger,
        transcription_service=mock_transcription_service,
        translation_service=mock_translation_service,
    )


@pytest.mark.asyncio
async def test_execute_success_no_translation(
    use_case: TranscribeFileToTextUseCase,
    mock_transcription_service: Mock,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_transcription_service.transcribe = AsyncMock(
        return_value=TranscriptionResultModel(text="transcription_result", segments=[]),
    )

    # When
    result = await use_case.execute(mock_file, "en", None)

    # Then
    assert result == "transcription_result"
    mock_transcription_service.transcribe.assert_awaited_once_with(mock_file, "en")
    mock_translation_service.translate_text.assert_not_called()


@pytest.mark.asyncio
async def test_execute_success_with_translation(
    use_case: TranscribeFileToTextUseCase,
    mock_transcription_service: Mock,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_transcription_service.transcribe = AsyncMock(
        return_value=TranscriptionResultModel(text="transcription_result", segments=[]),
    )
    mock_translation_service.translate_text = Mock(return_value="translated_result")

    # When
    result = await use_case.execute(mock_file, "en", "pl")

    # Then
    assert result == "translated_result"
    mock_transcription_service.transcribe.assert_awaited_once_with(mock_file, "en")
    mock_translation_service.translate_text.assert_called_once_with("transcription_result", "en", "pl")


@pytest.mark.asyncio
async def test_execute_failure(
    use_case: TranscribeFileToTextUseCase,
    mock_transcription_service: Mock,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_transcription_service.transcribe = AsyncMock(side_effect=Exception("Transcription error"))

    # When
    with pytest.raises(Exception, match="Transcription error"):
        await use_case.execute(mock_file, "en", "pl")

    # Then
    mock_transcription_service.transcribe.assert_awaited_once_with(mock_file, "en")
    mock_translation_service.translate_text.assert_not_called()
