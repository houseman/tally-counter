"""Tally Counter."""

from __future__ import annotations

import threading

from typing import Any

from .series import _Series


class Counter:
    """A container for any number of named data series."""

    def __init__(self, *args: str, **kwargs: int) -> None:
        # Thread safety lock
        self._lock = threading.RLock()

        ttl = self._get_int_or_none(kwargs, "ttl")
        maxlen = self._get_int_or_none(kwargs, "maxlen")

        init_data: dict[str, _Series] = {}
        for k in args:
            init_data[str(k)] = _Series(None, ttl=ttl, maxlen=maxlen, lock=self._lock)

        for k, v in kwargs.items():
            init_data[str(k)] = _Series(int(v), ttl=ttl, maxlen=maxlen, lock=self._lock)

        with self._lock:
            self.__data = init_data
            self.__ttl = ttl
            self.__maxlen = maxlen

    @property
    def data(self) -> dict[str, list[tuple[int, int]]]:
        """Return all data for this counter."""
        with self._lock:
            return {k: v.data for k, v in self.__data.items()}

    @property
    def ttl(self) -> int | None:
        """Return thr `ttl` property."""
        with self._lock:
            return self.__ttl

    def __getattr__(self, name: str) -> _Series:
        """
        Return a data series for the given attribute name.

        If no data series exists for the given name, then create an empty series and
        return that.
        """
        return self._get_or_create_series(key=name)

    def __getitem__(self, key: str) -> _Series:
        """
        Return a data series for the given key value.

        If no data series exists for the given key, then create an empty series and
        return that.
        """
        return self._get_or_create_series(key=key)

    @staticmethod
    def _get_int_or_none(container: dict[str, Any], key: str) -> int | None:
        try:
            return int(container.pop(key))
        except KeyError:
            return None
        except ValueError as e:
            message = f"'int' expected for argument '{key}'"
            raise TypeError(message) from e

    def _get_or_create_series(self, key: str) -> _Series:
        with self._lock:
            if key not in self.__data:
                self.__data[key] = _Series(None, ttl=self.__ttl, maxlen=self.__maxlen, lock=self._lock)

            return self.__data[key]
