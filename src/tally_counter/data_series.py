from __future__ import annotations

import math
import time

from typing_extensions import Self

from .data_point import DataPoint


class DataSeries:
    def __init__(self, initial_value: float = 0, *, ttl: int | None = None) -> None:
        self.__data_points = [DataPoint(initial_value)]
        self.__ttl = ttl

    def average(self) -> float:
        """
        Return the average float value for this data series
        """

        return sum([dp.value for dp in self.__data_points]) / len(self.__data_points)

    def age(self) -> int:
        """
        Return the age of this data series, in nanoseconds
        """

        return time.monotonic_ns() - self.__data_points[0].timestamp

    def time_span(self) -> int:
        """
        Return the time span of this data series, in nanoseconds
        """

        return self.__data_points[-1].timestamp - self.__data_points[0].timestamp

    @property
    def sum(self) -> float:
        return sum([dp.value for dp in self.__data_points])

    def __prune_data(self) -> None:
        """
        Prune data that has passed TTL from series, if a TTL is specified.
        """

        if not self.__ttl:
            return None

        ttl_in_ns = self.__ttl * 1000000  # 1 ms = 1000000 ns
        prune_ts = time.monotonic_ns() - ttl_in_ns

        self.__data_points = [
            dp for dp in self.__data_points if dp.timestamp > prune_ts
        ]

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
            self.__data_points.extend(other.__data_points)

            return self

        if isinstance(other, (int, float)):
            self.__data_points.append(DataPoint(float(other)))

            return self

        raise TypeError(
            f"unsupported operand type(s) for +: '{self.__class__.__name__}' and "
            f"'{type(other).__name__}'"
        )

    def __repr__(self) -> str:
        return f"{self.sum}"
