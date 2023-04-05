import re

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


def test_inequality_non_numeric_str():
    assert DataSeries(1) != "1"
    assert DataSeries(1) != "1.0"
    assert DataSeries(1) != "foo"


def test_invalid_equality_type():
    assert DataSeries(1) != ["foo"]


def test_repr():
    assert f"{DataSeries(1)}" == "1"


def test_addition_overloading():
    data_series = DataSeries(1)
    data_series += 9.0
    assert data_series == 10
    data_series += 199.0
    assert data_series == 209


def test_addition_overloading_raises_type_error():
    data_series = DataSeries(1000)
    with pytest.raises(
        TypeError,
        match=re.escape("unsupported operand type(s) for +: 'DataSeries' and 'str'"),
    ):
        data_series += "9.0"


def test_average():
    data_series = DataSeries()
    data_series += 13456
    data_series += 10234
    data_series += 454545
    data_series += 3445453656

    assert data_series.average() == 689186378.2


def test_age(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1001, 1002, 1003, 1004, 1005])

    data_series = DataSeries()
    data_series += 1
    data_series += 2
    data_series += 3

    assert data_series.age() == 4  # 1005 - 1001


def test_time_spam(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1001, 1002, 1003, 1004])

    data_series = DataSeries()
    data_series += 1
    data_series += 2
    data_series += 3

    assert data_series.time_span() == 3  # 1004 - 1001
