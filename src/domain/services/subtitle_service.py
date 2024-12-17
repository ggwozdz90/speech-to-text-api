from domain.models.transcription_result_model import TranscriptionResultModel


class SubtitleService:
    def convert_to_srt(
        self,
        transcription_result: TranscriptionResultModel,
    ) -> str:
        srt = []
        for i, segment in enumerate(transcription_result.segments, start=1):
            start_time = self._format_time(segment.start)
            end_time = self._format_time(segment.end)
            srt.append(f"{i}\n{start_time} --> {end_time}\n{segment.text}\n")
        return "\n".join(srt)

    def _format_time(
        self,
        seconds: float,
    ) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = round((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"
