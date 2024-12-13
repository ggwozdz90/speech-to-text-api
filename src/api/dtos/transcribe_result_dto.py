from pydantic import BaseModel


class TranscribeResultDTO(BaseModel):
    filename: str
    content: str
