from typing import Annotated, List

from fastapi import Depends

from config.logger_config import Logger
from domain.models.subtitle_segment_model import SubtitleSegmentModel
from domain.models.transcription_result_model import TranscriptionResultModel


class SubtitleService:
    def __init__(
        self,
        logger: Annotated[Logger, Depends()],
    ) -> None:
        self.logger = logger

    def convert_to_subtitle_segments(
        self,
        transcription_result: TranscriptionResultModel,
    ) -> List[SubtitleSegmentModel]:
        self.logger.info("Converting transcription result to subtitle segments")

        srt_segments = []

        for i, segment in enumerate(transcription_result.segments, start=1):
            start_time = self._format_time(segment.start)
            end_time = self._format_time(segment.end)
            time_range = f"{start_time} --> {end_time}"
            srt_segments.append(
                SubtitleSegmentModel(
                    counter=str(i),
                    time_range=time_range,
                    text=segment.text,
                )
            )

        self.logger.info("Conversion to subtitle segments completed")
        return srt_segments

    def generate_srt_result(
        self,
        srt_segments: List[SubtitleSegmentModel],
    ) -> str:
        self.logger.info("Generating SRT result from subtitle segments")

        srt_result = "\n".join(
            [f"{segment.counter}\n{segment.time_range}\n{segment.text.strip()}\n" for segment in srt_segments]
        )

        self.logger.info("SRT result generation completed")

        return srt_result

    def _format_time(
        self,
        seconds: float,
    ) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = round((seconds - int(seconds)) * 1000)

        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"
