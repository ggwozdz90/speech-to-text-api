class WorkerNotRunningError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Worker process is not running")
