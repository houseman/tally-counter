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
    data_series = DataSeries(1)
    data_series.incr(-1)
    data_series.incr()
    assert data_series == 3


def test_decr():
    data_series = DataSeries(1)
    data_series.decr(-1)
    data_series.decr()
    assert data_series == -1


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


def test_average():
    data_series = DataSeries()
    data_series.incr(13456)
    data_series.incr(10234)
    data_series.incr(454545)
    data_series.incr(3445453656)

    assert data_series.average() == 861482972.75


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


def test_prune_data_has_ttl(mocker):
    mocker.patch(
        "time.monotonic_ns",
        side_effect=[1000000, 2000000, 3000000, 4000000, 5000000, 6000000],
    )

    data_series = DataSeries(ttl=2)  # ttl=2ms == 2000000ns
    data_series.incr()  # timestamp == 1000000
    data_series.incr()  # timestamp == 2000000
    data_series.incr()  # timestamp == 3000000
    data_series.incr()  # timestamp == 4000000
    data_series.incr()  # timestamp == 5000000

    # Should prune anything < (6000000 - 2000000ns) == 4000000
    data_series._prune_data()
    assert len(data_series.dump()) == 2
    assert data_series.dump()[0] == (1, 4000000)
    assert data_series.dump()[1] == (1, 5000000)


def test_prune_data_no_ttl(mocker):
    mocker.patch("time.monotonic_ns", side_effect=[1, 2, 3, 4, 5])

    data_series = DataSeries()
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()
    data_series.incr()

    # Should prune nothing
    data_series._prune_data()
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
