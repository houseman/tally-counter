import pytest

from tally_counter.data_point import DataPoint
from tally_counter.data_series import DataSeries


@pytest.mark.parametrize(
    ["data_series", "expected"],
    [
        (DataSeries(10), 10.0),
        (DataSeries(100.0), 100),
        (DataSeries(100.01), 100.01),
        (DataSeries(100.01), DataPoint(100.01)),
        (DataSeries(100.01), DataSeries(100.01)),
    ],
)
def test_equality(data_series, expected):
    assert data_series == expected


@pytest.mark.parametrize(
    ["data_series", "expected"],
    [
        (DataSeries(100.01), 100.0),
        (DataSeries(100.01), DataPoint(100.1)),
        (DataSeries(100.01), DataSeries(100)),
    ],
)
def test_inequality(data_series, expected):
    assert data_series != expected


def test_valid_equality_numeric_str():
    assert DataSeries(1) == "1"
    assert DataSeries(1) == "1.0"


def test_inequality_non_numeric_str():
    assert DataSeries(1) != "foo"


def test_invalid_equality_type():
    assert DataSeries(1) != ["foo"]


def test_repr():
    assert f"{DataSeries(1)}" == "1"
