from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import PlainTextResponse

from api.dtos.language_dto import LanguageDTO
from api.dtos.transcribe_text_result_dto import TranscribeTextResultDTO
from application.usecases.transcribe_file_to_srt_usecase import (
    TranscribeFileToSrtUseCase,
)
from application.usecases.transcribe_file_to_text_usecase import (
    TranscribeFileToTextUseCase,
)
from core.logger.logger import Logger


class TranscribeRouter:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.post("/transcribe")(self.transcribe)
        self.router.post("/transcribe/srt")(self.transcribe_srt)

    async def transcribe(
        self,
        transcribe_file_to_text_usecase: Annotated[TranscribeFileToTextUseCase, Depends()],
        logger: Annotated[Logger, Depends()],
        file: UploadFile = File(...),
        source_language: str = Query(...),
        target_language: Optional[str] = Query(None),
    ) -> TranscribeTextResultDTO:
        logger.info(
            f"Received request to transcribe file: {file.filename} "
            f"with source language {source_language} and target language {target_language or 'none'}"
        )
        source_language_dto = LanguageDTO(language=source_language)
        target_language_dto = LanguageDTO(language=target_language) if target_language else None

        result = await transcribe_file_to_text_usecase.execute(
            file,
            source_language_dto.language,
            target_language_dto.language if target_language_dto else None,
        )

        logger.info(f"Transcription request for file {file.filename} completed")
        return TranscribeTextResultDTO(
            filename=file.filename or "unknown",
            content=result,
        )

    async def transcribe_srt(
        self,
        transcribe_file_to_srt_usecase: Annotated[TranscribeFileToSrtUseCase, Depends()],
        logger: Annotated[Logger, Depends()],
        file: UploadFile = File(...),
        source_language: str = Query(...),
        target_language: Optional[str] = Query(None),
    ) -> PlainTextResponse:
        logger.info(
            f"Received request to transcribe file to SRT: {file.filename} "
            f"with source language {source_language} and target language {target_language or 'none'}"
        )
        source_language_dto = LanguageDTO(language=source_language)
        target_language_dto = LanguageDTO(language=target_language) if target_language else None

        result = await transcribe_file_to_srt_usecase.execute(
            file,
            source_language_dto.language,
            target_language_dto.language if target_language_dto else None,
        )

        logger.info(f"Transcription to SRT request for file {file.filename} completed")
        return PlainTextResponse(content=result)
