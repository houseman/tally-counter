from __future__ import annotations

from typing import NamedTuple


class DataPoint(NamedTuple):
    """
    Represents a data point, which is a single integer value within a data series.

    A data point typically represents a single measurement, taken at a specified time
    point.
    """

    value: int
    timestamp: int
