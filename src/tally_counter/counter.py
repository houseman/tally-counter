from dataclasses import dataclass

from .data_series import DataSeries


@dataclass
class Counter:
    def __init__(self, **kwargs: float) -> None:
        try:
            ttl = int(kwargs.pop("ttl"))
        except KeyError:
            ttl = None
        except ValueError:
            raise TypeError("'int' expected for argument 'ttl'")

        if not kwargs:
            raise TypeError(f"{self.__class__.__name__} expects at least 1 attribute")

        self.__dict__.update(
            {
                str(k): DataSeries(initial_value=float(v), ttl=ttl)
                for k, v in kwargs.items()
            }
        )
