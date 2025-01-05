import json
import os
import threading
from typing import Optional


class LanguageMappingService:
    _instance: Optional["LanguageMappingService"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "LanguageMappingService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LanguageMappingService, cls).__new__(cls)
                    cls._instance._initialize()

        return cls._instance

    def _initialize(self) -> None:
        self.whisper_mapping = self.load_mapping("whisper_mapping.json")
        self.mbart_mapping = self.load_mapping("mbart_mapping.json")
        self.seamless_mapping = self.load_mapping("seamless_mapping.json")

    def load_mapping(self, filename: str) -> dict[str, str]:
        filepath = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "mappings", filename)
        with open(filepath, "r", encoding="utf-8") as file:
            return dict(sorted(json.load(file).items()))

    def map_language(self, language: str, model_type: str) -> str:
        try:
            if model_type == "openai/whisper":
                return self.whisper_mapping[language]
            elif model_type == "facebook/mbart-large-50-many-to-many-mmt":
                return self.mbart_mapping[language]
            elif model_type == "facebook/seamless-m4t-v2-large":
                return self.seamless_mapping[language]
            else:
                raise ValueError(f"Unknown model type: {model_type}")
        except KeyError:
            raise ValueError(f"Language '{language}' not found for model type '{model_type}'")
