import pytest

"""
Fixtures for doctests in `README.md`
"""


@pytest.fixture(autouse=True)
def patch_time(mocker):
    side_effect = list(
        range(11116073274, 11116650774, 2500)
    )  # Adjust this number if test change. This is fragile...
    side_effect.append(11116650774)

    mocker.patch("time.monotonic_ns", side_effect=side_effect)
