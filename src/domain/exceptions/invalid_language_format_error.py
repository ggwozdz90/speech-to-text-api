class InvalidLanguageFormatError(ValueError):
    def __init__(self) -> None:
        super().__init__("Invalid language format. Expected format is xx_XX")
