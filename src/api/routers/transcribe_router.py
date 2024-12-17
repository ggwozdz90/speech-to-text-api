from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.dtos.transcribe_srt_result_dto import TranscribeSrtResultDTO
from api.dtos.transcribe_text_result_dto import TranscribeTextResultDTO
from application.usecases.transcribe_file_to_srt_usecase import (
    TranscribeFileToSrtUseCase,
)
from application.usecases.transcribe_file_to_text_usecase import (
    TranscribeFileToTextUseCase,
)


class TranscribeRouter:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.post("/transcribe")(self.transcribe)
        self.router.post("/transcribe/srt")(self.transcribe_srt)

    async def transcribe(
        self,
        transcribe_file_to_text_usecase: Annotated[TranscribeFileToTextUseCase, Depends()],
        file: UploadFile = File(...),
        language: str = "en",
    ) -> TranscribeTextResultDTO:
        try:
            result = await transcribe_file_to_text_usecase.execute(file, language)
            return TranscribeTextResultDTO(
                filename=file.filename or "unknown",
                content=result,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def transcribe_srt(
        self,
        transcribe_file_to_srt_usecase: Annotated[TranscribeFileToSrtUseCase, Depends()],
        file: UploadFile = File(...),
        language: str = "en",
    ) -> TranscribeSrtResultDTO:
        try:
            result = await transcribe_file_to_srt_usecase.execute(file, language)
            return TranscribeSrtResultDTO(
                filename=file.filename or "unknown",
                srt_content=result,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
