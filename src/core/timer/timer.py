import threading
from typing import Callable, Optional

from domain.exceptions.invalid_interval_error import InvalidIntervalError


class Timer:
    def __init__(self) -> None:
        self.interval: float = 0.0
        self.function: Optional[Callable] = None  # type: ignore
        self._timer: Optional[threading.Timer] = None
        self._cancelled: bool = False

    def _reset_timer(self) -> None:
        if self._timer:
            self._timer.cancel()

        if not self._cancelled:
            self._timer = threading.Timer(self.interval, self._execute)
            self._timer.start()

    def start(
        self,
        interval: int,
        function: Callable,  # type: ignore
    ) -> None:
        if interval <= 0:
            raise InvalidIntervalError()

        self.interval = interval
        self.function = function
        self._cancelled = False
        self._reset_timer()

    def _execute(self) -> None:
        if self.function and not self._cancelled:
            self.function()
            self._reset_timer()

    def cancel(self) -> None:
        self._cancelled = True
        if self._timer:
            self._timer.cancel()
            self._timer = None


class TimerFactory:
    def create(self) -> "Timer":
        return Timer()
