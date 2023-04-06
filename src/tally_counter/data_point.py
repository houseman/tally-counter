from __future__ import annotations


class DataPoint:
    def __init__(self, value: float, ts: int) -> None:
        self.__value = value
        self.__ts = ts

    @property
    def value(self) -> float:
        """
        This data point's float value
        """

        return self.__value

    @property
    def timestamp(self) -> int:
        """
        This data point's monotonic timestamp
        """

        return self.__ts
