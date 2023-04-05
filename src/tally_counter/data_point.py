from __future__ import annotations

import time


class DataPoint:
    def __init__(self, value: float) -> None:
        self._value = value
        self._ts = time.monotonic_ns()

    @property
    def value(self) -> float:
        """
        This data point's float value
        """

        return self._value
