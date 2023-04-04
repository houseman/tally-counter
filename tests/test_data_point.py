from tally_counter.data_point import DataPoint


def test_value_property():
    assert DataPoint(1010).value == 1010
