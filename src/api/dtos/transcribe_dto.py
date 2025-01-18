import re
from typing import Any, Dict, Optional

from pydantic import BaseModel, field_validator

from domain.exceptions.invalid_language_format_error import InvalidLanguageFormatError


class TranscribeDTO(BaseModel):
    source_language: str
    target_language: Optional[str] = None
    transcription_parameters: Dict[str, Any] = {}
    translation_parameters: Dict[str, Any] = {}

    @staticmethod
    def validate_language_format(v: str) -> str:
        if not re.match(r"^[a-z]{2}_[A-Z]{2}$", v):
            raise InvalidLanguageFormatError()

        return v

    @field_validator("source_language")
    def validate_source_language(cls, v: str) -> str:
        return cls.validate_language_format(v)

    @field_validator("target_language")
    def validate_target_language(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return cls.validate_language_format(v)

        return v
