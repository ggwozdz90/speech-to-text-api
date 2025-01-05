from abc import ABC, abstractmethod


class SpeechToTextRepository(ABC):
    @abstractmethod
    def transcribe(self, file_path: str, language: str) -> dict[str, str]:
        pass
