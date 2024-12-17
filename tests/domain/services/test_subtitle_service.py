import pytest

from domain.models.transcription_result_model import (
    SegmentModel,
    TranscriptionResultModel,
)
from src.domain.services.subtitle_service import SubtitleService


@pytest.fixture
def subtitle_service() -> SubtitleService:
    return SubtitleService()


def test_convert_to_srt_success(subtitle_service: SubtitleService) -> None:
    # Given
    segments = [
        SegmentModel(
            id=1,
            start=0.0,
            end=1.0,
            seek=0,
            text="Hello",
            tokens=[],
            temperature=0.0,
            avg_logprob=0.0,
            compression_ratio=0.0,
            no_speech_prob=0.0,
        ),
        SegmentModel(
            id=2,
            start=1.0,
            end=2.0,
            seek=0,
            text="World",
            tokens=[],
            temperature=0.0,
            avg_logprob=0.0,
            compression_ratio=0.0,
            no_speech_prob=0.0,
        ),
    ]
    transcription_result = TranscriptionResultModel(segments=segments, text="Hello World")

    expected_srt = "1\n00:00:00,000 --> 00:00:01,000\nHello\n\n" "2\n00:00:01,000 --> 00:00:02,000\nWorld\n"

    # When
    result = subtitle_service.convert_to_srt(transcription_result)

    # Then
    assert result == expected_srt


def test_convert_to_srt_empty_segments(subtitle_service: SubtitleService) -> None:
    # Given
    transcription_result = TranscriptionResultModel(segments=[], text="")

    # When
    result = subtitle_service.convert_to_srt(transcription_result)

    # Then
    assert result == ""


def test_format_time(subtitle_service: SubtitleService) -> None:
    # Given
    seconds = 3661.123  # 1 hour, 1 minute, 1 second, and 123 milliseconds
    expected_time = "01:01:01,123"

    # When
    result = subtitle_service._format_time(seconds)

    # Then
    assert result == expected_time


def test_format_time_zero(subtitle_service: SubtitleService) -> None:
    # Given
    seconds = 0.0
    expected_time = "00:00:00,000"

    # When
    result = subtitle_service._format_time(seconds)

    # Then
    assert result == expected_time


def test_format_time_edge_case(subtitle_service: SubtitleService) -> None:
    # Given
    seconds = 3599.999  # 59 minutes, 59 seconds, and 999 milliseconds
    expected_time = "00:59:59,999"

    # When
    result = subtitle_service._format_time(seconds)

    # Then
    assert result == expected_time
