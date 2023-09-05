"""`DataSeries` unit tests."""

import math
import re

import pytest

from tally_counter.data_point import DataPoint
from tally_counter.data_series import DataSeries


def test_init():
    assert DataSeries() == 0
    assert DataSeries(1) == 1
    assert DataSeries(DataPoint(123, 1000)) == 123


@pytest.mark.parametrize(
    ["data_series", "expected"],
    [
        (DataSeries(10), 10),
        (DataSeries(100), DataPoint(100, 0)),
        (DataSeries(100), DataSeries(100)),
    ],
)
def test_equality(data_series, expected):
    assert data_series == expected


@pytest.mark.parametrize(
    ["data_series", "expected"],
    [
        (DataSeries(100), 10),
        (DataSeries(100), DataPoint(10, 0)),
        (DataSeries(100), DataSeries(10)),
    ],
)
def test_inequality(data_series, expected):
    assert data_series != expected


def test_inequality_non_numeric_str():
    assert DataSeries(1) != "1"
    assert DataSeries(1) != "1"
    assert DataSeries(1) != "foo"


def test_invalid_equality_type():
    assert DataSeries(1) != ["foo"]


def test_repr():
    assert f"{DataSeries(1)}" == "1"


def test_incr():
    data_series = DataSeries(100)
    data_series.incr(-10)  # +(-10) == -10
    data_series.incr(10)  # +(+10) == +10
    data_series.incr()  # +(+1) == +1
    assert data_series == 101


def test_decr():
    data_series = DataSeries(100)
    data_series.decr(-10)  # -(-10) == +10
    data_series.decr(10)  # -(+10) == -10
    data_series.decr()  # -(+1) == -1
    assert data_series == 99


def test_incr_raises_type_error():
    with pytest.raises(
        TypeError, match=re.escape("incr() argument must be an integer, not 'str'")
    ):
        DataSeries().incr("foo")


def test_decr_raises_type_error():
    with pytest.raises(
        TypeError, match=re.escape("decr() argument must be an integer, not 'str'")
    ):
        DataSeries().decr("foo")


@pytest.fixture
def data_series():
    data_series = DataSeries()
    data_series.incr(13456)
    data_series.incr(10234)
    data_series.incr(454545)
    data_series.decr(6548794)
    data_series.incr(3445453656)
    data_series.decr(101)

    return data_series


def test_mean(data_series):
    assert math.isclose(data_series.mean(), 573230499.8333334)


def test_mean_p95(data_series):
    data_series = DataSeries()
    for i in range(1, 1001):
        data_series.incr(i)

    expected = sum(range(1, 950)) / 949
    assert math.isclose(data_series.mean(95), expected)


def test_min(data_series):
    assert data_series.min() == -6548794


def test_max(data_series):
    assert data_series.max() == 3445453656


def test_max_p95():
    data_series = DataSeries()
    for i in range(1, 1001):
        data_series.incr(i)

    assert data_series.max(95) == 949


def test_age(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1001, 1002, 1003, 1004, 1005])

    data_series = DataSeries()
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()

    assert data_series.age() == 4  # 1005 - 1001


def test_time_spam(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1001, 1002, 1003, 1004])

    data_series = DataSeries()
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()

    assert data_series.span() == 3  # 1004 - 1001


def test_prune_has_maxlen(mocker):
    mocker.patch(
        "time.monotonic_ns",
        side_effect=[i * 1000 for i in range(1, 1001)],
    )

    data_series = DataSeries(maxlen=100)
    for i in range(1, 1001):
        data_series.incr(i)

    # Should prune length to 100
    assert data_series.len() == 100
    assert data_series.dump()[0] == (901, 901000)
    assert data_series.dump()[-1] == (1000, 1000000)


def test_prune_has_ttl(mocker):
    mocker.patch(
        "time.monotonic_ns",
        side_effect=[i * 10000 for i in range(1, 4000)],
    )

    data_series = DataSeries(ttl=2)  # ttl=2ms == 2000000ns
    for i in range(1, 1001):
        data_series.incr(i)

    assert data_series.dump()[0] == (901, 18010000)
    assert data_series.dump()[-1] == (1000, 19990000)


def test_prune_no_ttl(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1, 2, 3, 4, 5])

    data_series = DataSeries()
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()

    # Should prune nothing
    data_series._prune()
    assert len(data_series.dump()) == 5


def test_len():
    data_series = DataSeries(1)
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()

    assert data_series.len() == 5


def test_dump():
    data_series = DataSeries()
    data_series.incr(1022, timestamp=1000)
    data_series.incr(1023, timestamp=1001)
    data_series.incr(1024, timestamp=1002)

    assert data_series.dump() == [(1022, 1000), (1023, 1001), (1024, 1002)]


def test_get_percentile_exception(data_series):
    with pytest.raises(ValueError):
        data_series._get_percentile(data_series._pruned(), 100)
