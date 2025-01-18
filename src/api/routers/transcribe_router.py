from typing import Annotated, Any, Dict, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
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
        file: UploadFile = File(...),
        source_language: str = Form(...),
        target_language: Optional[str] = Form(None),
        transcription_parameters: Dict[str, Any] = Form({}),
        translation_parameters: Dict[str, Any] = Form({}),
    ) -> TranscribeTextResultDTO:
        transcribe_dto = TranscribeDTO(
            source_language=source_language,
            target_language=target_language,
            transcription_parameters=transcription_parameters,
            translation_parameters=translation_parameters,
        )

        transcription = await transcribe_file_to_text_usecase.execute(
            file,
            transcribe_dto.source_language,
            transcribe_dto.target_language,
            transcribe_dto.transcription_parameters,
            transcribe_dto.translation_parameters,
        )

        return TranscribeTextResultDTO(
            transcription=transcription,
        )

    async def transcribe_srt(
        self,
        transcribe_file_to_srt_usecase: Annotated[TranscribeFileToSrtUseCase, Depends()],
        file: UploadFile = File(...),
        source_language: str = Form(...),
        target_language: Optional[str] = Form(None),
        transcription_parameters: Dict[str, Any] = Form({}),
        translation_parameters: Dict[str, Any] = Form({}),
    ) -> PlainTextResponse:
        transcribe_dto = TranscribeDTO(
            source_language=source_language,
            target_language=target_language,
            transcription_parameters=transcription_parameters,
            translation_parameters=translation_parameters,
        )

        srt = await transcribe_file_to_srt_usecase.execute(
            file,
            transcribe_dto.source_language,
            transcribe_dto.target_language,
            transcribe_dto.transcription_parameters,
            transcribe_dto.translation_parameters,
        )

        return PlainTextResponse(content=srt)
