from __future__ import annotations

import time


class DataPoint:
    def __init__(self, value: float) -> None:
        self.__value = value
        self.__ts = time.monotonic_ns()

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
