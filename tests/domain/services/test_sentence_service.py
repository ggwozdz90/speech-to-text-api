from unittest.mock import Mock

import pytest

from core.logger.logger import Logger
from src.domain.models.sentence_model import SentenceModel
from src.domain.models.subtitle_segment_model import SubtitleSegmentModel
from src.domain.services.sentence_service import SentenceService


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def sentence_service(mock_logger: Logger) -> SentenceService:
    return SentenceService(logger=mock_logger)


@pytest.fixture
def mock_segment() -> Mock:
    return Mock(spec=SubtitleSegmentModel)


def test_create_sentence_models_single_segment(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    mock_segment.text = "This is a test."
    mock_segment.counter = "1"
    segments = [mock_segment]

    # When
    result = sentence_service.create_sentence_models(segments)

    # Then
    assert len(result) == 1
    assert result[0].text == "This is a test."
    assert result[0].segment_percentage == {"1": 1.0}


def test_create_sentence_models_multiple_segments(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    mock_segment_1 = Mock(spec=SubtitleSegmentModel)
    mock_segment_1.text = "This is a test"
    mock_segment_1.counter = "1"

    mock_segment_2 = Mock(spec=SubtitleSegmentModel)
    mock_segment_2.text = "sentence."
    mock_segment_2.counter = "2"

    segments = [mock_segment_1, mock_segment_2]

    # When
    result = sentence_service.create_sentence_models(segments)

    # Then
    assert len(result) == 1
    assert result[0].text == "This is a test sentence."
    assert result[0].segment_percentage == {"1": 0.8, "2": 0.2}


def test_create_sentence_models_no_punctuation(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    mock_segment.text = "This is a test without punctuation"
    mock_segment.counter = "1"
    segments = [mock_segment]

    # When
    result = sentence_service.create_sentence_models(segments)

    # Then
    assert len(result) == 1
    assert result[0].text == "This is a test without punctuation"
    assert result[0].segment_percentage == {"1": 1.0}


def test_create_sentence_models_multiple_sentences(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    mock_segment_1 = Mock(spec=SubtitleSegmentModel)
    mock_segment_1.text = "First sentence."
    mock_segment_1.counter = "1"

    mock_segment_2 = Mock(spec=SubtitleSegmentModel)
    mock_segment_2.text = "Second sentence."
    mock_segment_2.counter = "2"

    segments = [mock_segment_1, mock_segment_2]

    # When
    result = sentence_service.create_sentence_models(segments)

    # Then
    assert len(result) == 2
    assert result[0].text == "First sentence."
    assert result[0].segment_percentage == {"1": 1.0}
    assert result[1].text == "Second sentence."
    assert result[1].segment_percentage == {"2": 1.0}


def test_create_sentence_models_split_segments(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    mock_segment_1 = Mock(spec=SubtitleSegmentModel)
    mock_segment_1.text = "The quick brown"
    mock_segment_1.counter = "1"

    mock_segment_2 = Mock(spec=SubtitleSegmentModel)
    mock_segment_2.text = "fox jumps over the lazy dog. The"
    mock_segment_2.counter = "2"

    mock_segment_3 = Mock(spec=SubtitleSegmentModel)
    mock_segment_3.text = "dog is very lazy."
    mock_segment_3.counter = "3"

    segments = [mock_segment_1, mock_segment_2, mock_segment_3]

    # When
    result = sentence_service.create_sentence_models(segments)

    # Then
    assert len(result) == 2
    assert result[0].text == "The quick brown fox jumps over the lazy dog."
    assert result[0].segment_percentage == {"1": 0.33, "2": 0.67}
    assert result[1].text == "The dog is very lazy."
    assert result[1].segment_percentage == {"2": 0.20, "3": 0.80}


def test_apply_translated_sentences_single_sentence(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    translated_sentences = [SentenceModel(text="This is a test.", segment_percentage={"1": 1.0})]
    segments = [mock_segment]
    mock_segment.counter = "1"

    # When
    sentence_service.apply_translated_sentences(segments, translated_sentences)

    # Then
    assert mock_segment.text == "This is a test."


def test_apply_translated_sentences_multiple_sentences(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    translated_sentences = [
        SentenceModel(text="First sentence.", segment_percentage={"1": 1.0}),
        SentenceModel(text="Second sentence.", segment_percentage={"2": 1.0}),
    ]
    mock_segment_1 = Mock(spec=SubtitleSegmentModel)
    mock_segment_1.counter = "1"
    mock_segment_2 = Mock(spec=SubtitleSegmentModel)
    mock_segment_2.counter = "2"
    segments = [mock_segment_1, mock_segment_2]

    # When
    sentence_service.apply_translated_sentences(segments, translated_sentences)

    # Then
    assert mock_segment_1.text == "First sentence."
    assert mock_segment_2.text == "Second sentence."


def test_apply_translated_sentences_split_segments(sentence_service: SentenceService, mock_segment: Mock) -> None:
    # Given
    translated_sentences = [
        SentenceModel(text="The quick brown fox jumps over the lazy dog.", segment_percentage={"1": 0.33, "2": 0.67}),
        SentenceModel(text="The dog is very lazy.", segment_percentage={"2": 0.20, "3": 0.80}),
    ]
    mock_segment_1 = Mock(spec=SubtitleSegmentModel)
    mock_segment_1.counter = "1"
    mock_segment_2 = Mock(spec=SubtitleSegmentModel)
    mock_segment_2.counter = "2"
    mock_segment_3 = Mock(spec=SubtitleSegmentModel)
    mock_segment_3.counter = "3"
    segments = [mock_segment_1, mock_segment_2, mock_segment_3]

    # When
    sentence_service.apply_translated_sentences(segments, translated_sentences)

    # Then
    assert mock_segment_1.text == "The quick brown"
    assert mock_segment_2.text == "fox jumps over the lazy dog. The"
    assert mock_segment_3.text == "dog is very lazy."
