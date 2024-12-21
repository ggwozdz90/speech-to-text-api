from abc import ABC, abstractmethod


class TranslationModelRepository(ABC):
    @abstractmethod
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        pass
