from typing import Dict

from pydantic import BaseModel


class SentenceModel(BaseModel):
    text: str
    segment_percentage: Dict[str, float]
