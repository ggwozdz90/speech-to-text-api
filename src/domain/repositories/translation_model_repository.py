from abc import ABC, abstractmethod
from typing import Any, Dict


class TranslationModelRepository(ABC):
    @abstractmethod
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        translation_parameters: Dict[str, Any],
    ) -> str:
        pass
