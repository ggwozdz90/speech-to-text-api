class UnsupportedModelConfigurationError(ValueError):
    def __init__(self, model_name: str) -> None:
        super().__init__(f"Unsupported model name: {model_name}")
