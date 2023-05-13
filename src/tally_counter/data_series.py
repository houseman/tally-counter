from __future__ import annotations

import threading
import time

from .data_point import DataPoint


class DataSeries:
    """
    Represents a data series, a linear sequence of data points, ordered by point in time
    """

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
        """
        Increment the count for this data series by default of `1` or specified `value`.
        """

        try:
            self._append(abs(value), timestamp=timestamp)
        except TypeError:
            raise TypeError(
                f"incr() argument must be an integer, not '{value.__class__.__name__}'"
            )

    def decr(self, value: int = 1, /, *, timestamp: int | None = None) -> None:
        """
        Decrement the count for this data series by default of `-1` or specified `value`
        """

        try:
            self._append(-abs(value), timestamp=timestamp)
        except TypeError:
            raise TypeError(
                f"decr() argument must be an integer, not '{value.__class__.__name__}'"
            )

    def _append(self, value: int = 1, /, *, timestamp: int | None = None) -> None:
        """
        This should be the only function that mutates (appends to) the data points list
        """

        if timestamp is None:
            timestamp = time.monotonic_ns()

        with self._lock:
            self.__data_points.append(DataPoint(int(value), timestamp))
            self._prune()  # Pruned after adding data

    def average(self) -> float:
        """
        Return the average float value for this data series
        """

        with self._lock:
            data_points = self._pruned()
            return sum([dp.value for dp in data_points]) / len(data_points)

    def len(self) -> int:
        """
        Return the length (number of data points) of this data series
        """

        with self._lock:
            return len(self._pruned())

    def age(self) -> int:
        """
        Return the age of this data series, in nanoseconds
        """

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
        with self._lock:
            return [dp.dump() for dp in self._pruned()]

    @property
    def sum(self) -> int:
        with self._lock:
            return sum([dp.value for dp in self._pruned()])

    def _prune(self) -> None:
        """
        Prune data from the series, that has
        - passed TTL from series, if a TTL is specified. Or,
        - exceeds the maximum series length, ordered by time descending
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

    def _pruned(self) -> list[DataPoint]:
        self._prune
        return self.__data_points

    def __eq__(self, other: object) -> bool:
        """
        Overloads the `==` operator.
        """

        if isinstance(other, DataPoint):
            return self.sum == other.value

        if isinstance(other, DataSeries):
            return self.sum == other.sum

        if isinstance(other, int):
            return self.sum == other

        return False

    def __repr__(self) -> str:
        return f"{self.sum}"
