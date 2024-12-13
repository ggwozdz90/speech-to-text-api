from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.dtos.transcribe_result_dto import TranscribeResultDTO
from application.usecases.file_transcribe_usecase import FileTranscribeUseCase


class TranscribeRouter:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.post("/transcribe")(self.transcribe)

    async def transcribe(
        self,
        file_transcribe_usecase: Annotated[FileTranscribeUseCase, Depends()],
        file: UploadFile = File(...),
        language: str = "en",
    ) -> TranscribeResultDTO:
        try:
            result = await file_transcribe_usecase.execute(file, language)

            return TranscribeResultDTO(
                filename=file.filename or "unknown",
                content=result,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
