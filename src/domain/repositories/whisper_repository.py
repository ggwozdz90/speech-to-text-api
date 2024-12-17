from abc import ABC, abstractmethod


class WhisperRepository(ABC):
    @abstractmethod
    def transcribe(self, file_path: str, language: str) -> dict[str, str]:
        pass
