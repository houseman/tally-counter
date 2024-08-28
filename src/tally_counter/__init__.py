"""Tally Counter."""

import importlib.metadata

from .counter import Counter

__all__ = ["Counter"]

__version__ = importlib.metadata.version("tally_counter")
