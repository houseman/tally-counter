"""Tally Counter."""
from __future__ import annotations

import threading

from typing import Any

from .data_series import DataSeries


class Counter:
    """Represents a container for any number of named data series."""

    def __init__(self, *args: str, **kwargs: int) -> None:
        # Thread safety lock
        self._lock = threading.RLock()

        ttl = self._get_int_or_none(kwargs, "ttl")
        maxlen = self._get_int_or_none(kwargs, "maxlen")

        init_data: dict[str, DataSeries] = {}
        for k in args:
            init_data[str(k)] = DataSeries(None, ttl=ttl, maxlen=maxlen)

        for k, v in kwargs.items():
            init_data[str(k)] = DataSeries(int(v), ttl=ttl, maxlen=maxlen)

        with self._lock:
            self.__data = init_data
            self.__ttl = ttl
            self.__maxlen = maxlen

    def dump(self) -> dict[str, list[tuple[int, int]]]:
        """Return all data items."""
        with self._lock:
            return {k: v.dump() for k, v in self.__data.items()}

    @property
    def ttl(self) -> int | None:
        """Return thr `ttl` property."""
        with self._lock:
            return self.__ttl

    def __getattr__(self, name: str) -> DataSeries:
        """
        Find and return a data series for the given attribute name.

        If no data series exists for the given name, then create an empty series and
        return that.
        """
        return self._get_key_val(key=name)

    def __getitem__(self, key: str) -> DataSeries:
        """
        Find and return a data series for the given key value.

        If no data series exists for the given key, then create an empty series and
        return that.
        """
        return self._get_key_val(key=key)

    @staticmethod
    def _get_int_or_none(container: dict[str, Any], key: str) -> int | None:
        try:
            return int(container.pop(key))
        except KeyError:
            return None
        except ValueError as e:
            raise TypeError(f"'int' expected for argument '{key}'") from e

    def _get_key_val(self, key: str) -> DataSeries:
        with self._lock:
            if key not in self.__data:
                self.__data[key] = DataSeries(
                    None, ttl=self.__ttl, maxlen=self.__maxlen
                )

            return self.__data[key]
