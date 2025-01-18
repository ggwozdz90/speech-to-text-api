import pytest
from pydantic import ValidationError

from api.dtos.transcribe_text_result_dto import TranscribeTextResultDTO


@pytest.fixture
def valid_data() -> dict[str, str]:
    return {
        "transcription": "transcription result",
    }


@pytest.fixture
def invalid_data() -> dict[str, str]:
    return {
        # Missing 'content' field
    }


def test_transcribe_test_result_dto_valid(valid_data: dict[str, str]) -> None:
    # When
    dto = TranscribeTextResultDTO(**valid_data)

    # Then
    assert dto.transcription == valid_data["transcription"]


def test_transcribe_test_result_dto_invalid(invalid_data: dict[str, str]) -> None:
    # When / Then
    with pytest.raises(ValidationError):
        TranscribeTextResultDTO(**invalid_data)


def test_transcribe_test_result_dto_empty_content() -> None:
    # Given
    data = {
        "transcription": "",
    }

    # When
    dto = TranscribeTextResultDTO(**data)

    # Then
    assert dto.transcription == data["transcription"]
