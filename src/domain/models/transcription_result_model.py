from typing import List

from pydantic import BaseModel


class SegmentModel(BaseModel):
    id: int
    seek: int
    start: float
    end: float
    text: str
    tokens: List[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float


class TranscriptionResultModel(BaseModel):
    text: str
    segments: List[SegmentModel]
