from abc import ABC, abstractmethod
from typing import Any, Dict


class SpeechToTextRepository(ABC):
    @abstractmethod
    def transcribe(
        self,
        file_path: str,
        language: str,
        transcription_parameters: Dict[str, Any],
    ) -> dict[str, str]:
        pass
