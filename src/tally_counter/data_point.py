"""The `DataPoint` model."""
from __future__ import annotations

import threading


class DataPoint:
    """
    Represents a data point, which is a single integer value within a data series.

    A data point typically represents a single measurement, taken at a specified time
    point.
    """

    def __init__(self, value: int, timestamp: int) -> None:
        self._lock = threading.RLock()
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

    def dump(self) -> tuple[int, int]:
        """Return data point values."""
        with self._lock:
            return (self.__value, self.__timestamp)
