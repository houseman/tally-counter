from __future__ import annotations

import math
import time

from .data_point import DataPoint


class DataSeries:
    """
    Represents a data series, a sequence of data points indexed in time order.
    """

    def __init__(
        self, initial_value: int | DataPoint | None = None, /, *, ttl: int | None = None
    ) -> None:
        self.__ttl = ttl
        self.__data_points: list[DataPoint] = []

        if initial_value is not None:
            if isinstance(initial_value, DataPoint):
                self.__data_points.append(initial_value)
            else:
                self.__data_points.append(
                    DataPoint(int(initial_value), time.monotonic_ns())
                )

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
        if timestamp is None:
            timestamp = time.monotonic_ns()

        self.__data_points.append(DataPoint(int(value), timestamp))

    def average(self) -> float:
        """
        Return the average float value for this data series
        """

        return sum([dp.value for dp in self.__data_points]) / len(self.__data_points)

    def len(self) -> int:
        """
        Return the length (number of data points) of this data series
        """

        return len(self.__data_points)

    def age(self) -> int:
        """
        Return the age of this data series, in nanoseconds
        """

        return time.monotonic_ns() - self.__data_points[0].timestamp

    def span(self) -> int:
        """
        Return the time span of this data series, in nanoseconds
        """

        return self.__data_points[-1].timestamp - self.__data_points[0].timestamp

    def dump(self) -> list[tuple]:
        return [dp.dump() for dp in self.__data_points]

    @property
    def sum(self) -> int:
        return sum([dp.value for dp in self.__data_points])

    def _prune_data(self) -> None:
        """
        Prune data that has passed TTL from series, if a TTL is specified.
        """

        if not self.__ttl:
            return None

        ttl_in_ns = self.__ttl * 1000000  # 1 ms = 1000000 ns
        prune_ts = time.monotonic_ns() - ttl_in_ns

        self.__data_points = [
            dp for dp in self.__data_points if dp.timestamp >= prune_ts
        ]

    def __eq__(self, other: object) -> bool:
        """
        Overloads the `==` operator.
        """

        if isinstance(other, DataPoint):
            return self.sum == other.value

        if isinstance(other, DataSeries):
            return self.sum == other.sum

        if isinstance(other, int):
            return math.isclose(self.sum, other)

        return False

    def __repr__(self) -> str:
        return f"{self.sum}"
