"""`_Series` unit tests."""

import math
import re

import pytest

from tally_counter.point import _Point
from tally_counter.series import _Series


def test_init():
    assert _Series() == 0
    assert _Series(1) == 1
    assert _Series(_Point(123, 1000)) == 123


@pytest.mark.parametrize(
    ("series", "expected"),
    [
        (_Series(10), 10),
        (_Series(100), _Point(100, 0)),
        (_Series(100), _Series(100)),
    ],
)
def test_equality(series, expected):
    assert series == expected


@pytest.mark.parametrize(
    ("series", "expected"),
    [
        (_Series(100), 10),
        (_Series(100), _Point(10, 0)),
        (_Series(100), _Series(10)),
    ],
)
def test_inequality(series, expected):
    assert series != expected


def test_inequality_non_numeric_str():
    assert _Series(1) != "1"
    assert _Series(1) != "1"
    assert _Series(1) != "foo"


def test_invalid_equality_type():
    assert _Series(1) != ["foo"]


def test_repr():
    assert f"{_Series(1)}" == "1"


def test_incr():
    series = _Series(100)
    series.incr(-10)  # +(-10) == -10
    series.incr(10)  # +(+10) == +10
    series.incr()  # +(+1) == +1
    assert series == 101


def test_decr():
    series = _Series(100)
    series.decr(-10)  # -(-10) == +10
    series.decr(10)  # -(+10) == -10
    series.decr()  # -(+1) == -1
    assert series == 99


def test_incr_raises_type_error():
    with pytest.raises(TypeError, match=re.escape("incr() argument must be an integer, not 'str'")):
        _Series().incr("foo")


def test_decr_raises_type_error():
    with pytest.raises(TypeError, match=re.escape("decr() argument must be an integer, not 'str'")):
        _Series().decr("foo")


@pytest.fixture
def series():
    series = _Series()
    series.incr(13456)
    series.incr(10234)
    series.incr(454545)
    series.decr(6548794)
    series.incr(3445453656)
    series.decr(101)

    return series


def test_mean(series):
    assert math.isclose(series.mean(), 573230499.8333334)


def test_mean_p95(series):
    series = _Series()
    for i in range(1, 1001):
        series.incr(i)

    expected = sum(range(1, 950)) / 949
    assert math.isclose(series.mean(95), expected)


def test_min(series):
    assert series.min() == -6548794


def test_max(series):
    assert series.max() == 3445453656


def test_max_p95():
    series = _Series()
    for i in range(1, 1001):
        series.incr(i)

    assert series.max(95) == 949


def test_age(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1001, 1002, 1003, 1004, 1005])

    series = _Series()
    series.incr()
    series.incr()
    series.incr()
    series.incr()

    assert series.age() == 4  # 1005 - 1001


def test_time_spam(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1001, 1002, 1003, 1004])

    series = _Series()
    series.incr()
    series.incr()
    series.incr()
    series.incr()

    assert series.span() == 3  # 1004 - 1001


def test_prune_has_maxlen(mocker):
    mocker.patch(
        "time.monotonic_ns",
        side_effect=[i * 1000 for i in range(1, 1001)],
    )

    series = _Series(maxlen=100)
    for i in range(1, 1001):
        series.incr(i)

    # Should prune length to 100
    assert series.len() == 100
    assert series.data[0] == (901, 901000)
    assert series.data[-1] == (1000, 1000000)


def test_prune_has_ttl(mocker):
    mocker.patch(
        "time.monotonic_ns",
        side_effect=[i * 10000 for i in range(1, 4000)],
    )

    series = _Series(ttl=2)  # ttl=2ms == 2000000ns
    for i in range(1, 1001):
        series.incr(i)

    assert series.data[0] == (901, 18010000)
    assert series.data[-1] == (1000, 19990000)


def test_prune_no_ttl(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1, 2, 3, 4, 5])

    series = _Series()
    series.incr()
    series.incr()
    series.incr()
    series.incr()
    series.incr()

    # Should prune nothing
    series._prune()
    assert len(series.data) == 5


def test_len():
    series = _Series(1)
    series.incr()
    series.incr()
    series.incr()
    series.incr()

    assert series.len() == 5


def test_data():
    series = _Series()
    series.incr(1022, timestamp=1000)
    series.incr(1023, timestamp=1001)
    series.incr(1024, timestamp=1002)

    assert series.data == [(1022, 1000), (1023, 1001), (1024, 1002)]


def test_get_percentile_exception(series):
    with pytest.raises(ValueError, match="Percentile must be an integer from 1 to 99, not 100."):
        series._get_percentile(series._pruned(), 100)
