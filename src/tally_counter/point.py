"""The `_Point` model."""

from __future__ import annotations

import threading


class _Point:
    """
    Represents a data point, which is a single integer value within a data series.

    A data point typically represents a single measurement, taken at a specified time
    point.
    """

    def __init__(
        self,
        value: int,
        timestamp: int,
        lock: threading.RLock | None = None,
    ) -> None:
        if lock is None:
            lock = threading.RLock()
        self._lock = lock

        self.__value = int(value)
        self.__timestamp = int(timestamp)

    @property
    def value(self) -> int:
        """Return the data point's integer value."""
        with self._lock:
            return self.__value

    @property
    def timestamp(self) -> int:
        """Return the data point's monotonic timestamp."""
        with self._lock:
            return self.__timestamp

    @property
    def data(self) -> tuple[int, int]:
        """Return data point values."""
        with self._lock:
            return (self.__value, self.__timestamp)
