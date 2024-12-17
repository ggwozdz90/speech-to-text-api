from pydantic import BaseModel


class TranscribeTextResultDTO(BaseModel):
    filename: str
    content: str
