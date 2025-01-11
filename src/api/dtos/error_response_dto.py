from typing import Any, Dict, Optional

from pydantic import BaseModel


class ErrorResponseDto(BaseModel):
    status_code: int
    message: str
    details: Optional[Dict[str, Any]] = None
    trace: Optional[list[str]] = None
