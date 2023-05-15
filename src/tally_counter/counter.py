from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

from .data_series import DataSeries

if TYPE_CHECKING:
    from .data_point import DataPoint


class Counter:
    """
    Represents a container for any number of named data series.
    """

    def __init__(self, *args: str, **kwargs: int) -> None:
        # Thread safety lock
        self._lock = threading.RLock()

        ttl = self._get_int_from_kwargs(kwargs, "ttl")
        maxlen = self._get_int_from_kwargs(kwargs, "maxlen")

        init_data: dict[str, DataSeries] = {}
        for k in args:
            init_data[str(k)] = DataSeries(None, ttl=ttl, maxlen=maxlen)

        for k, v in kwargs.items():
            initial_value = None if v is None else int(v)

            init_data[str(k)] = DataSeries(initial_value, ttl=ttl, maxlen=maxlen)

        with self._lock:
            self.__data = init_data
            self.__ttl = ttl
            self.__maxlen = maxlen

    def dump(self) -> dict[str, list[DataPoint]]:
        with self._lock:
            return {k: v.dump() for k, v in self.__data.items()}

    @property
    def ttl(self) -> int | None:
        with self._lock:
            return self.__ttl

    def __getattr__(self, name: str) -> Any:
        """
        Called when an attribute lookup has not found the attribute in the usual places
        """

        with self._lock:
            data_series = self.__data.get(name)
            if not data_series:
                data_series = DataSeries(None, ttl=self.__ttl, maxlen=self.__maxlen)
                self.__data[name] = data_series

            return data_series

    @staticmethod
    def _get_int_from_kwargs(kwargs: dict[str, int], key: str) -> int | None:
        try:
            return int(kwargs.pop(key))
        except KeyError:
            return None
        except ValueError:
            raise TypeError(f"'int' expected for argument '{key}'")
