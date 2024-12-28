from abc import ABC, abstractmethod


class SpeachToTextRepository(ABC):
    @abstractmethod
    def transcribe(self, file_path: str, language: str) -> dict[str, str]:
        pass
