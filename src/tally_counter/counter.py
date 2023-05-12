from __future__ import annotations

import threading
from typing import Any

from .data_series import DataSeries


class Counter:
    """
    Represents a container for any number of named data series.
    """

    def __init__(self, *args: str, **kwargs: int) -> None:
        # Thread safety lock
        self.__lock = threading.RLock()

        try:
            ttl = int(kwargs.pop("ttl"))
        except KeyError:
            ttl = None
        except ValueError:
            raise TypeError("'int' expected for argument 'ttl'")

        init_data: dict[str, DataSeries] = {}
        for k in args:
            init_data[str(k)] = DataSeries(None, ttl=ttl)

        for k, v in kwargs.items():
            initial_value = None if v is None else int(v)

            init_data[str(k)] = DataSeries(initial_value, ttl=ttl)

        with self.__lock:
            self.__data = init_data
            self.__ttl = ttl

    def dump(self) -> dict[str, list[tuple]]:
        with self.__lock:
            return {k: v.dump() for k, v in self.__data.items()}

    @property
    def ttl(self) -> int | None:
        with self.__lock:
            return self.__ttl

    def __getattr__(self, name: str) -> Any:
        """
        Called when an attribute lookup has not found the attribute in the usual places
        """

        with self.__lock:
            data_series = self.__data.get(name)
            if not data_series:
                data_series = DataSeries(None, ttl=self.__ttl)
                self.__data[name] = data_series

            return data_series
