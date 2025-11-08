import time
from typing import Optional


class Timer:
    """Utility class for measuring algorithm execution time."""

    def __init__(self):
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._elapsed_time: float = 0.0

    def start(self) -> None:
        """Start the timer."""
        self._start_time = time.perf_counter()
        self._end_time = None
        self._elapsed_time = 0.0

    def stop(self) -> float:
        """Stop the timer and return elapsed time in seconds."""
        if self._start_time is None:
            raise RuntimeError("Timer was not started")

        self._end_time = time.perf_counter()
        self._elapsed_time = self._end_time - self._start_time
        return self._elapsed_time

    def get_elapsed(self) -> float:
        """Get elapsed time (even if timer is still running)."""
        if self._start_time is None:
            return 0.0

        if self._end_time is None:
            return time.perf_counter() - self._start_time

        return self._elapsed_time

    def reset(self) -> None:
        """Reset the timer."""
        self._start_time = None
        self._end_time = None
        self._elapsed_time = 0.0

    def format_time(self, precision: int = 4) -> str:
        """Format elapsed time as a readable string."""
        elapsed = self.get_elapsed()

        if elapsed < 0.001:
            return f"{elapsed * 1000000:.{precision}f} µs"
        elif elapsed < 1.0:
            return f"{elapsed * 1000:.{precision}f} ms"
        else:
            return f"{elapsed:.{precision}f} s"
