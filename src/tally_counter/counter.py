from dataclasses import dataclass

from .data_series import DataSeries


@dataclass
class Counter:
    def __init__(self, **kwargs: float) -> None:
        self.__dict__.update(
            {str(k): DataSeries(initial_value=float(v)) for k, v in kwargs.items()}
        )
