from typing import Annotated, Optional

from fastapi import Depends, UploadFile

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.models.subtitle_segment_model import SubtitleSegmentModel
from domain.services.sentence_service import SentenceService
from domain.services.subtitle_service import SubtitleService
from domain.services.transcription_service import TranscriptionService
from domain.services.translation_service import TranslationService


class TranscribeFileToSrtUseCase:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        logger: Annotated[Logger, Depends()],
        transcription_service: Annotated[TranscriptionService, Depends()],
        subtitle_service: Annotated[SubtitleService, Depends()],
        sentence_service: Annotated[SentenceService, Depends()],
        translation_service: Annotated[TranslationService, Depends()],
    ) -> None:
        self.config = config
        self.logger = logger
        self.transcription_service = transcription_service
        self.subtitle_service = subtitle_service
        self.sentence_service = sentence_service
        self.translation_service = translation_service

    def _generate_srt(
        self,
        subtitle_segments: list[SubtitleSegmentModel],
    ) -> str:
        srt_result: str = self.subtitle_service.generate_srt_result(subtitle_segments)
        return srt_result

    def _translate_subtitles(
        self,
        subtitle_segments: list[SubtitleSegmentModel],
        source_language: str,
        target_language: str,
    ) -> None:
        sentences = self.sentence_service.create_sentence_models(subtitle_segments)
        self.translation_service.translate_sentences(sentences, source_language, target_language)
        self.sentence_service.apply_translated_sentences(subtitle_segments, sentences)

    async def execute(
        self,
        file: UploadFile,
        source_language: str,
        target_language: Optional[str],
    ) -> str:
        self.logger.info(
            f"Executing transcription to SRT for file '{file.filename}' "
            f"from '{source_language}' to '{target_language}'",
        )

        transcription_result = await self.transcription_service.transcribe(file, source_language)
        subtitle_segments = self.subtitle_service.convert_to_subtitle_segments(transcription_result)

        if not target_language or source_language == target_language:
            self.logger.info(f"Returning SRT result for file '{file.filename}'")

            return self._generate_srt(subtitle_segments)

        self._translate_subtitles(subtitle_segments, source_language, target_language)

        self.logger.info(f"Returning translated SRT result for file '{file.filename}'")

        return self._generate_srt(subtitle_segments)
