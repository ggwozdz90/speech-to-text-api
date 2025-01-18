import pytest
from pydantic import ValidationError

from src.api.dtos.transcribe_dto import TranscribeDTO


def test_transcribe_dto_valid_languages() -> None:
    # Given
    valid_source_language = "en_US"
    valid_target_language = "es_ES"

    # When
    dto = TranscribeDTO(
        source_language=valid_source_language,
        target_language=valid_target_language,
        transcription_parameters={},
        translation_parameters={},
    )

    # Then
    assert dto.source_language == valid_source_language
    assert dto.target_language == valid_target_language
    assert dto.transcription_parameters == {}
    assert dto.translation_parameters == {}


def test_transcribe_dto_invalid_source_language() -> None:
    # Given
    invalid_source_language = "english_US"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        TranscribeDTO(
            source_language=invalid_source_language,
            target_language="es_ES",
            transcription_parameters={},
            translation_parameters={},
        )

    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_transcribe_dto_invalid_target_language() -> None:
    # Given
    invalid_target_language = "spanish_ES"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        TranscribeDTO(
            source_language="en_US",
            target_language=invalid_target_language,
            transcription_parameters={},
            translation_parameters={},
        )

    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_transcribe_dto_optional_target_language() -> None:
    # Given
    valid_source_language = "en_US"

    # When
    dto = TranscribeDTO(
        source_language=valid_source_language,
        transcription_parameters={},
        translation_parameters={},
    )

    # Then
    assert dto.source_language == valid_source_language
    assert dto.target_language is None
    assert dto.transcription_parameters == {}
    assert dto.translation_parameters == {}
