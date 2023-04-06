import pytest

"""
Fixtures for doctests in `README.md`
"""


@pytest.fixture(autouse=True)
def patch_time(mocker):
    side_effect = [11116073274 + (2500 * i) for i in range(0, 500)]

    mocker.patch("time.monotonic_ns", side_effect=side_effect)
