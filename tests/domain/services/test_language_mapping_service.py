import json
from unittest.mock import mock_open, patch

import pytest

from src.domain.services.language_mapping_service import LanguageMappingService


@pytest.fixture
def mock_mappings() -> dict[str, dict[str, str]]:
    return {
        "whisper_mapping.json": {"en": "English", "es": "Spanish"},
        "mbart_mapping.json": {"en": "English", "es": "Spanish"},
        "seamless_mapping.json": {"en": "English", "es": "Spanish"},
    }


@pytest.fixture
def language_mapping_service(mock_mappings: dict[str, dict[str, str]]) -> LanguageMappingService:
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_mappings["whisper_mapping.json"]))):
        with patch("os.path.join", return_value="whisper_mapping.json"):
            service = LanguageMappingService()

    return service


def test_map_language_whisper(language_mapping_service: LanguageMappingService) -> None:
    # Given
    language = "en"
    model_type = "openai/whisper"

    # When
    result = language_mapping_service.map_language(language, model_type)

    # Then
    assert result == "English"


def test_map_language_mbart(language_mapping_service: LanguageMappingService) -> None:
    # Given
    language = "es"
    model_type = "facebook/mbart-large-50-many-to-many-mmt"

    # When
    result = language_mapping_service.map_language(language, model_type)

    # Then
    assert result == "Spanish"


def test_map_language_seamless(language_mapping_service: LanguageMappingService) -> None:
    # Given
    language = "en"
    model_type = "facebook/seamless-m4t-v2-large"

    # When
    result = language_mapping_service.map_language(language, model_type)

    # Then
    assert result == "English"


def test_map_language_unknown_model(language_mapping_service: LanguageMappingService) -> None:
    # Given
    language = "en"
    model_type = "unknown_model"

    # When / Then
    with pytest.raises(ValueError, match="Unknown model type: unknown_model"):
        language_mapping_service.map_language(language, model_type)


def test_map_language_unknown_language(language_mapping_service: LanguageMappingService) -> None:
    # Given
    language = "fr"
    model_type = "openai/whisper"

    # When / Then
    with pytest.raises(ValueError, match="Language 'fr' not found for model type 'openai/whisper'"):
        language_mapping_service.map_language(language, model_type)
