from unittest.mock import Mock

import pytest
from fastapi import UploadFile
from pydantic import ValidationError

from src.api.dtos.transcribe_dto import TranscribeDTO


@pytest.fixture
def mock_upload_file() -> UploadFile:
    return Mock(UploadFile)


def test_transcribe_dto_valid_languages(mock_upload_file: UploadFile) -> None:
    # Given
    valid_source_language = "en_US"
    valid_target_language = "es_ES"

    # When
    dto = TranscribeDTO(
        source_language=valid_source_language, target_language=valid_target_language, file=mock_upload_file
    )

    # Then
    assert dto.source_language == valid_source_language
    assert dto.target_language == valid_target_language
    assert dto.file == mock_upload_file


def test_transcribe_dto_invalid_source_language(mock_upload_file: UploadFile) -> None:
    # Given
    invalid_source_language = "english_US"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        TranscribeDTO(source_language=invalid_source_language, target_language="es_ES", file=mock_upload_file)
    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_transcribe_dto_invalid_target_language(mock_upload_file: UploadFile) -> None:
    # Given
    invalid_target_language = "spanish_ES"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        TranscribeDTO(source_language="en_US", target_language=invalid_target_language, file=mock_upload_file)
    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_transcribe_dto_optional_target_language(mock_upload_file: UploadFile) -> None:
    # Given
    valid_source_language = "en_US"

    # When
    dto = TranscribeDTO(source_language=valid_source_language, file=mock_upload_file)

    # Then
    assert dto.source_language == valid_source_language
    assert dto.target_language is None
    assert dto.file == mock_upload_file
