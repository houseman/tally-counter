from __future__ import annotations

import math

from .data_point import DataPoint


class DataSeries:
    def __init__(self, initial_value: float) -> None:
        self._data_points = [DataPoint(value=initial_value)]

    @property
    def sum(self) -> float:
        return sum([dp._value for dp in self._data_points])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataPoint):
            return self.sum == other._value

        if isinstance(other, DataSeries):
            return self.sum == other.sum

        if isinstance(other, (int, float)):
            return math.isclose(self.sum, float(other))

        if isinstance(other, str):
            try:
                return math.isclose(self.sum, float(other))
            except ValueError:
                return False

        return False

    def __repr__(self) -> str:
        return f"{self.sum}"
