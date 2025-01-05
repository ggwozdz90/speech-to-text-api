class LanguageNotFoundError(KeyError):
    def __init__(self, language: str, model_type: str):
        super().__init__(f"Language '{language}' not found for model type '{model_type}'")
