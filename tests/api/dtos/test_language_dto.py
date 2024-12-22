import pytest
from pydantic import ValidationError

from src.api.dtos.language_dto import LanguageDTO


def test_language_dto_valid_language() -> None:
    # Given
    valid_language = "en_US"

    # When
    dto = LanguageDTO(language=valid_language)

    # Then
    assert dto.language == valid_language


def test_language_dto_invalid_language_format() -> None:
    # Given
    invalid_language = "english_USA"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        LanguageDTO(language=invalid_language)

    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_language_dto_empty_language() -> None:
    # Given
    empty_language = ""

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        LanguageDTO(language=empty_language)

    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_language_dto_missing_language() -> None:
    # Given / When / Then
    with pytest.raises(ValidationError) as exc_info:
        LanguageDTO(**{})

    assert "Field required" in str(exc_info.value)
