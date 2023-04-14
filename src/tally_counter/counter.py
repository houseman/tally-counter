from typing import Any

from .data_series import DataSeries


class Counter:
    def __init__(self, *args: str, **kwargs: float) -> None:
        try:
            ttl = int(kwargs.pop("ttl"))
        except KeyError:
            ttl = None
        except ValueError:
            raise TypeError("'int' expected for argument 'ttl'")

        data = {}
        for k in args:
            data[str(k)] = DataSeries(initial_value=None, ttl=ttl)

        for k, v in kwargs.items():
            initial_value = None if v is None else float(v)

            data[str(k)] = DataSeries(initial_value=initial_value, ttl=ttl)

        self._data = data
        self._ttl = ttl

    def __getattr__(self, name: str) -> Any:
        """
        Called when an attribute lookup has not found the attribute in the usual places
        """

        data_series = self._data.get(name)
        if not data_series:
            data_series = DataSeries(initial_value=None, ttl=self._ttl)
            self._data[name] = data_series

        return data_series
