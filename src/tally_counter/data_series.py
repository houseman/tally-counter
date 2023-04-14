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
        self._data_points: list[DataPoint] = []

        if initial_value is not None:
            if isinstance(initial_value, DataPoint):
                self._data_points.append(initial_value)
            else:
                self._data_points.append(
                    DataPoint(int(initial_value), time.monotonic_ns())
                )

    def incr(self, value: int = 1, /) -> None:
        """
        Increment the count for this data series by default of `1` or specified `value`.
        """

        if isinstance(value, int):
            self._data_points.append(DataPoint(value, time.monotonic_ns()))

            return

        raise TypeError(
            f"incr() argument must be an integer, not '{value.__class__.__name__}'"
        )

    def average(self) -> float:
        """
        Return the average float value for this data series
        """

        return sum([dp.value for dp in self._data_points]) / len(self._data_points)

    def len(self) -> int:
        """
        Return the length (number of data points) of this data series
        """

        return len(self._data_points)

    def age(self) -> int:
        """
        Return the age of this data series, in nanoseconds
        """

        return time.monotonic_ns() - self._data_points[0].timestamp

    def span(self) -> int:
        """
        Return the time span of this data series, in nanoseconds
        """

        return self._data_points[-1].timestamp - self._data_points[0].timestamp

    @property
    def sum(self) -> int:
        return sum([dp.value for dp in self._data_points])

    def _prune_data(self) -> None:
        """
        Prune data that has passed TTL from series, if a TTL is specified.
        """

        if not self.__ttl:
            return None

        ttl_in_ns = self.__ttl * 1000000  # 1 ms = 1000000 ns
        prune_ts = time.monotonic_ns() - ttl_in_ns

        self._data_points = [dp for dp in self._data_points if dp.timestamp >= prune_ts]

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
