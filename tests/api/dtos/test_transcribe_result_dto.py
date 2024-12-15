import pytest
from pydantic import ValidationError

from api.dtos.transcribe_result_dto import TranscribeResultDTO


@pytest.fixture
def valid_data() -> dict[str, str]:
    return {
        "filename": "test_file.txt",
        "content": "transcription result",
    }


@pytest.fixture
def invalid_data() -> dict[str, str]:
    return {
        "filename": "test_file.txt",
        # Missing 'content' field
    }


def test_transcribe_result_dto_valid(valid_data: dict[str, str]) -> None:
    # When
    dto = TranscribeResultDTO(**valid_data)

    # Then
    assert dto.filename == valid_data["filename"]
    assert dto.content == valid_data["content"]


def test_transcribe_result_dto_invalid(invalid_data: dict[str, str]) -> None:
    # When / Then
    with pytest.raises(ValidationError):
        TranscribeResultDTO(**invalid_data)


def test_transcribe_result_dto_empty_content() -> None:
    # Given
    data = {
        "filename": "test_file.txt",
        "content": "",
    }

    # When
    dto = TranscribeResultDTO(**data)

    # Then
    assert dto.filename == data["filename"]
    assert dto.content == data["content"]


def test_transcribe_result_dto_invalid_filename_type() -> None:
    # Given
    data = {
        "filename": 123,  # Invalid type
        "content": "transcription result",
    }

    # When / Then
    with pytest.raises(ValidationError):
        TranscribeResultDTO(**data)
