import re

from pydantic import BaseModel, field_validator


class LanguageDTO(BaseModel):
    language: str

    @field_validator("language")
    def validate_language(
        cls,
        v: str,
    ) -> str:
        if not re.match(r"^[a-z]{2}_[A-Z]{2}$", v):
            raise ValueError("Invalid language format. Expected format is xx_XX")
        return v
