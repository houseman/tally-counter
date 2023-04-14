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

        data = {}
        for k, v in kwargs.items():
            initial_value = None if v is None else float(v)

            data[str(k)] = DataSeries(initial_value=initial_value, ttl=ttl)

        self.__dict__.update(data)
