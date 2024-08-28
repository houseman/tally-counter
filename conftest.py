"""Fixtures for doctests in `README.md`."""

import pytest


@pytest.fixture(autouse=True)
def patch_time(mocker):
    """Patch the `time.monotonic_ns` method for consistency."""
    side_effect = [11116073274 + (2500 * i) for i in range(1500)]

    mocker.patch("time.monotonic_ns", side_effect=side_effect)
