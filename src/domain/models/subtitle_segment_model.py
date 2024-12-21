from pydantic import BaseModel


class SubtitleSegmentModel(BaseModel):
    counter: str
    time_range: str
    text: str
