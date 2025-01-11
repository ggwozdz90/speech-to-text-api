from typing import Dict, Optional

from pydantic import BaseModel


class SentenceModel(BaseModel):
    text: str
    translation: Optional[str] = None
    segment_percentage: Dict[str, float]
