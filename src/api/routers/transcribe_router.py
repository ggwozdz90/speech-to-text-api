from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from api.dtos.transcribe_dto import TranscribeDTO
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
        transcribe_dto: TranscribeDTO = Depends(),
    ) -> TranscribeTextResultDTO:
        result = await transcribe_file_to_text_usecase.execute(
            transcribe_dto.file,
            transcribe_dto.source_language,
            transcribe_dto.target_language,
        )

        return TranscribeTextResultDTO(
            filename=transcribe_dto.file.filename or "unknown",
            content=result,
        )

    async def transcribe_srt(
        self,
        transcribe_file_to_srt_usecase: Annotated[TranscribeFileToSrtUseCase, Depends()],
        transcribe_dto: TranscribeDTO = Depends(),
    ) -> PlainTextResponse:
        result = await transcribe_file_to_srt_usecase.execute(
            transcribe_dto.file,
            transcribe_dto.source_language,
            transcribe_dto.target_language,
        )

        return PlainTextResponse(content=result)
