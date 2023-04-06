from __future__ import annotations

import math
import time

from typing_extensions import Self

from .data_point import DataPoint


class DataSeries:
    def __init__(
        self, initial_value: float | DataPoint | None = None, *, ttl: int | None = None
    ) -> None:
        if initial_value is None:
            initial_value = 0.0

        if isinstance(initial_value, (float, int)):
            initial_value = DataPoint(float(initial_value), time.monotonic_ns())

        self._data_points = [initial_value]
        self.__ttl = ttl

    def average(self) -> float:
        """
        Return the average float value for this data series
        """

        return sum([dp.value for dp in self._data_points]) / len(self._data_points)

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
    def sum(self) -> float:
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

        if isinstance(other, (int, float)):
            return math.isclose(self.sum, float(other))

        return False

    def __add__(self, other: object) -> Self:
        """
        Overloads the `+` operator.
        """

        if isinstance(other, DataSeries):
            self._data_points.extend(other._data_points)

            return self

        if isinstance(other, DataPoint):
            self._data_points.append(other)

            return self

        if isinstance(other, (int, float)):
            self._data_points.append(DataPoint(float(other), time.monotonic_ns()))

            return self

        raise TypeError(
            f"unsupported operand type(s) for +: '{self.__class__.__name__}' and "
            f"'{type(other).__name__}'"
        )

    def __repr__(self) -> str:
        return f"{self.sum}"
