class InvalidFileNameError(ValueError):
    def __init__(self) -> None:
        super().__init__("Invalid file name")
