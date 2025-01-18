from pydantic import BaseModel


class TranscribeTextResultDTO(BaseModel):
    transcription: str
