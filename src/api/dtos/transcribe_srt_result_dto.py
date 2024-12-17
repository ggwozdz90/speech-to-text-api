from pydantic import BaseModel


class TranscribeSrtResultDTO(BaseModel):
    filename: str
    srt_content: str
