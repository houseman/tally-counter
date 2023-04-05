import pytest

"""
Fixtures for doctests in `README.md`
"""


@pytest.fixture(autouse=True)
def patch_time(mocker):
    side_effect = [0] * 203  # Adjust this number if test change. Flakey, I know...
    side_effect.append(606490)

    mocker.patch("time.monotonic_ns", side_effect=side_effect)
