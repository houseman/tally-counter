from __future__ import annotations


class DataPoint:
    """
    Represents a data point, which is a single integer value within a data series.

    A data point typically represents a single measurement, taken at a specified time
    point.
    """

    def __init__(self, value: int, timestamp: int) -> None:
        self.__value = int(value)
        self.__timestamp = int(timestamp)

    @property
    def value(self) -> int:
        """
        This data point's integer value
        """

        return self.__value

    @property
    def timestamp(self) -> int:
        """
        This data point's monotonic timestamp
        """

        return self.__timestamp

    def dump(self) -> tuple[int, int]:
        return (self.__value, self.__timestamp)
