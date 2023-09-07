"""`_Point` unit tests."""


def test_properties():
    from tally_counter.point import _Point

    point = _Point(1010, 1000)

    assert point.value == 1010
    assert point.timestamp == 1000


def test_dump():
    from tally_counter.point import _Point

    assert _Point(100, 10000).data == (100, 10000)
