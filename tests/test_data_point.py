def test_properties():
    from tally_counter.data_point import DataPoint

    data_point = DataPoint(1010, 1000)

    assert data_point.value == 1010
    assert data_point.timestamp == 1000


def test_dump():
    from tally_counter.data_point import DataPoint

    assert DataPoint(100, 10000).dump() == (100, 10000)
