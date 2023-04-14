from __future__ import annotations


class DataPoint:
    def __init__(self, value: int, ts: int) -> None:
        self.__value = int(value)
        self.__ts = int(ts)

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

        return self.__ts
