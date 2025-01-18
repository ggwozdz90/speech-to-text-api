from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.services.sentence_service import SentenceService
from domain.services.subtitle_service import SubtitleService
from domain.services.transcription_service import TranscriptionService
from domain.services.translation_service import TranslationService
from src.application.usecases.transcribe_file_to_srt_usecase import (
    TranscribeFileToSrtUseCase,
)


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_transcription_service() -> TranscriptionService:
    return Mock(TranscriptionService)


@pytest.fixture
def mock_subtitle_service() -> Mock:
    return Mock(SubtitleService)


@pytest.fixture
def mock_sentence_service() -> SentenceService:
    return Mock(SentenceService)


@pytest.fixture
def mock_translation_service() -> TranslationService:
    return Mock(TranslationService)


@pytest.fixture
def usecase(
    mock_config: Mock,
    mock_logger: Mock,
    mock_transcription_service: Mock,
    mock_subtitle_service: Mock,
    mock_sentence_service: Mock,
    mock_translation_service: Mock,
) -> TranscribeFileToSrtUseCase:
    return TranscribeFileToSrtUseCase(
        config=mock_config,
        logger=mock_logger,
        transcription_service=mock_transcription_service,
        subtitle_service=mock_subtitle_service,
        sentence_service=mock_sentence_service,
        translation_service=mock_translation_service,
    )


@pytest.mark.asyncio
async def test_execute_success_no_translation(
    usecase: TranscribeFileToSrtUseCase,
    mock_transcription_service: Mock,
    mock_subtitle_service: Mock,
    mock_sentence_service: Mock,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_transcription_service.transcribe = AsyncMock(return_value="transcription_result")
    mock_subtitle_service.convert_to_subtitle_segments.return_value = ["segment1", "segment2"]
    mock_subtitle_service.generate_srt_result.return_value = "srt_result"

    # When
    result = await usecase.execute(mock_file, "en", None, {}, {})

    # Then
    assert result == "srt_result"
    mock_transcription_service.transcribe.assert_awaited_once_with(mock_file, "en", {})
    mock_subtitle_service.convert_to_subtitle_segments.assert_called_once_with("transcription_result")
    mock_subtitle_service.generate_srt_result.assert_called_once_with(["segment1", "segment2"])
    mock_sentence_service.create_sentence_models.assert_not_called()
    mock_translation_service.translate_sentences.assert_not_called()
    mock_sentence_service.apply_translated_sentences.assert_not_called()


@pytest.mark.asyncio
async def test_execute_success_with_translation(
    usecase: TranscribeFileToSrtUseCase,
    mock_transcription_service: Mock,
    mock_subtitle_service: Mock,
    mock_sentence_service: Mock,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_transcription_service.transcribe = AsyncMock(return_value="transcription_result")
    mock_subtitle_service.convert_to_subtitle_segments.return_value = ["segment1", "segment2"]
    mock_sentence_service.create_sentence_models.return_value = ["sentence1", "sentence2"]
    mock_translation_service.translate_sentences.return_value = ["translated_sentence1", "translated_sentence2"]
    mock_sentence_service.apply_translated_sentences.return_value = ["translated_segment1", "translated_segment2"]
    mock_subtitle_service.generate_srt_result.return_value = "translated_srt_result"

    # When
    result = await usecase.execute(mock_file, "en", "pl", {}, {})

    # Then
    assert result == "translated_srt_result"
    mock_transcription_service.transcribe.assert_awaited_once_with(mock_file, "en", {})
    mock_subtitle_service.convert_to_subtitle_segments.assert_called_once_with("transcription_result")
    mock_sentence_service.create_sentence_models.assert_called_once_with(["segment1", "segment2"])
    mock_translation_service.translate_sentences.assert_called_once_with(["sentence1", "sentence2"], "en", "pl", {})
    mock_sentence_service.apply_translated_sentences.assert_called_once_with(
        ["segment1", "segment2"],
        ["sentence1", "sentence2"],
    )
    mock_subtitle_service.generate_srt_result.assert_called_once_with(["segment1", "segment2"])


@pytest.mark.asyncio
async def test_execute_failure(
    usecase: TranscribeFileToSrtUseCase,
    mock_transcription_service: Mock,
    mock_subtitle_service: Mock,
    mock_sentence_service: Mock,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_file = Mock(UploadFile)
    mock_file.filename = "test_file.txt"
    mock_transcription_service.transcribe = AsyncMock(side_effect=Exception("Transcription error"))

    # When
    with pytest.raises(Exception, match="Transcription error"):
        await usecase.execute(mock_file, "en", "pl", {}, {})

    # Then
    mock_transcription_service.transcribe.assert_awaited_once_with(mock_file, "en", {})
    mock_subtitle_service.convert_to_subtitle_segments.assert_not_called()
    mock_sentence_service.create_sentence_models.assert_not_called()
    mock_translation_service.translate_sentences.assert_not_called()
    mock_sentence_service.apply_translated_sentences.assert_not_called()
    mock_subtitle_service.generate_srt_result.assert_not_called()
