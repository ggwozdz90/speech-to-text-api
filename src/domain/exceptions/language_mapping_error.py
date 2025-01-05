class LanguageMappingError(ValueError):
    def __init__(self, model_type: str):
        super().__init__(f"Error loading language mappings for model type: {model_type}")
