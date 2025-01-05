class InvalidIntervalError(ValueError):
    def __init__(self) -> None:
        super().__init__("Interval must be greater than 0")
