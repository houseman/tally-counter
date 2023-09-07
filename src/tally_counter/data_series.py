"""The `DataSeries` model."""

from __future__ import annotations

import math
import threading
import time

from .data_point import DataPoint


class DataSeries:
    """Represents a data series, a linear sequence of data points, ordered by time."""

    def __init__(
        self,
        initial_value: int | DataPoint | None = None,
        /,
        *,
        ttl: int | None = None,
        maxlen: int | None = None,
    ) -> None:
        self._lock = threading.RLock()
        self.__ttl = ttl
        self.__maxlen = maxlen
        self.__data_points: list[DataPoint] = []

        if initial_value is not None:
            with self._lock:
                if isinstance(initial_value, DataPoint):
                    self._append(initial_value.value, timestamp=initial_value.timestamp)
                else:
                    self._append(int(initial_value), timestamp=time.monotonic_ns())

    def incr(self, value: int = 1, /, *, timestamp: int | None = None) -> None:
        """Increment the count for this data series by default of `1` or `value`."""
        try:
            self._append(+(value), timestamp=timestamp)
        except TypeError as e:
            raise TypeError(
                f"incr() argument must be an integer, not '{value.__class__.__name__}'"
            ) from e

    def decr(self, value: int = 1, /, *, timestamp: int | None = None) -> None:
        """Decrement the count for this data series by default of `-1` or `value`."""
        try:
            self._append(-(value), timestamp=timestamp)
        except TypeError as e:
            raise TypeError(
                f"decr() argument must be an integer, not '{value.__class__.__name__}'"
            ) from e

    def _append(self, value: int = 1, /, *, timestamp: int | None = None) -> None:
        """Only use this method to mutate (append to) the data points list."""
        if timestamp is None:
            timestamp = time.monotonic_ns()

        with self._lock:
            self.__data_points.append(DataPoint(int(value), timestamp))
            self._prune()  # Pruned after adding data

    def mean(self, percentile: int = 0) -> float:
        """Return the mean float value for this data series."""
        with self._lock:
            data_points = self._pruned(percentile)
            return sum([dp.value for dp in data_points]) / len(data_points)

    def min(self) -> int:
        """Return the minimum value for this data series."""
        with self._lock:
            data_points = self._pruned()
            return min([dp.value for dp in data_points])

    def max(self, percentile: int = 0) -> int:
        """Return the maximum value for this data series."""
        with self._lock:
            data_points = self._pruned(percentile)
            return max([dp.value for dp in data_points])

    def len(self) -> int:
        """Return the length (number of data points) of this data series."""
        with self._lock:
            return len(self._pruned())

    def age(self) -> int:
        """Return the age of this data series, in nanoseconds."""
        return time.monotonic_ns() - self._pruned()[0].timestamp

    def span(self) -> int:
        """
        Return the time span of this data series, in nanoseconds.

        This is the time difference between the earliest and latest data points in the
        series.
        """
        with self._lock:
            data_points = self._pruned()

            return data_points[-1].timestamp - data_points[0].timestamp

    def dump(self) -> list[tuple[int, int]]:
        """Return all series data."""
        with self._lock:
            return [dp.dump() for dp in self._pruned()]

    @property
    def sum(self) -> int:
        """Return the sum of this data series."""
        with self._lock:
            return sum([dp.value for dp in self._pruned()])

    def _prune(self) -> None:
        """
        Prune data from the series, that has.

        - passed TTL from series, if a TTL is specified. Or,
        - exceeds the maximum series length, ordered by time descending.
        """
        with self._lock:
            # Prune by age
            if self.__ttl:
                ttl_in_ns = self.__ttl * 1000000  # 1 ms = 1000000 ns
                prune_ts = time.monotonic_ns() - ttl_in_ns

                self.__data_points = [
                    dp for dp in self.__data_points if dp.timestamp >= prune_ts
                ]

            # Prune length
            if self.__maxlen and len(self.__data_points) > self.__maxlen:
                self.__data_points = self.__data_points[-self.__maxlen :]

    def _pruned(self, percentile: int = 0) -> list[DataPoint]:
        self._prune()
        if percentile:
            return self._get_percentile(self.__data_points, percentile=percentile)

        return self.__data_points

    def _get_percentile(
        self, data_points: list[DataPoint], percentile: int
    ) -> list[DataPoint]:
        """Return the requested percentile from the given data series."""
        if not 100 > percentile > 1:  # noqa: PLR2004
            raise ValueError(
                f"Percentile must be an integer from 1 to 99, not {percentile}."
            )

        with self._lock:
            size = len(data_points)  # Length of the data series
            percentile_point = math.floor(size * (percentile / 100))  # percentile point

            return data_points[0 : percentile_point - 1]

    def __eq__(self, other: object) -> bool:
        """Overloads the `==` operator."""
        if isinstance(other, DataPoint):
            return self.sum == other.value

        if isinstance(other, DataSeries):
            return self.sum == other.sum

        if isinstance(other, int):
            return self.sum == other

        return False

    def __repr__(self) -> str:
        """Return the representation of this instance."""
        return f"{self.sum}"
