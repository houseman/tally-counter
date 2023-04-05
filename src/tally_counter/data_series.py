from __future__ import annotations

import math
import time

from typing_extensions import Self

from .data_point import DataPoint


class DataSeries:
    def __init__(self, initial_value: float = 0) -> None:
        self._data_points = [DataPoint(value=initial_value)]

    def average(self) -> float:
        """
        Return the average float value for this data series
        """

        return sum([dp._value for dp in self._data_points]) / len(self._data_points)

    def age(self) -> int:
        """
        Return the age of this data series, in nanoseconds
        """

        return time.monotonic_ns() - self._data_points[0]._ts

    def time_span(self) -> int:
        """
        Return the time span of this data series, in nanoseconds
        """

        return self._data_points[-1]._ts - self._data_points[0]._ts

    @property
    def sum(self) -> float:
        return sum([dp._value for dp in self._data_points])

    def __eq__(self, other: object) -> bool:
        """
        Overloads the `==` operator.
        """

        if isinstance(other, DataPoint):
            return self.sum == other._value

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

        if isinstance(other, (int, float)):
            self._data_points.append(DataPoint(float(other)))

            return self

        raise TypeError(
            f"unsupported operand type(s) for +: '{self.__class__.__name__}' and "
            f"'{type(other).__name__}'"
        )

    def __repr__(self) -> str:
        return f"{self.sum}"
