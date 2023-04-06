from tally_counter.data_point import DataPoint


def test_properties():
    data_point = DataPoint(1010, 1000)

    assert data_point.value == 1010
    assert data_point.timestamp == 1000
