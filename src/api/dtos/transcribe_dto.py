import re
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, field_validator


class TranscribeDTO(BaseModel):
    source_language: str
    target_language: Optional[str] = None
    file: UploadFile

    @staticmethod
    def validate_language_format(v: str) -> str:
        if not re.match(r"^[a-z]{2}_[A-Z]{2}$", v):
            raise ValueError("Invalid language format. Expected format is xx_XX")

        return v

    @field_validator("source_language")
    def validate_source_language(cls, v: str) -> str:
        return cls.validate_language_format(v)

    @field_validator("target_language")
    def validate_target_language(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return cls.validate_language_format(v)

        return v
