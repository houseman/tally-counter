"""`_Point` unit tests."""


def test_init__positional_arguments():
    """
    Test the initialization of a `_Point` object with valid arguments

    Given: A `_Point` class from the `tally_counter` module.
    When: A `_Point` object is created with positional arguments
    Then: A object attribute values are set
    """
    from tally_counter.point import _Point

    point = _Point(1010, 1000)

    assert point.value == 1010
    assert point.timestamp == 1000


def test_init__keyword_arguments():
    """
    Test the initialization of a `_Point` object with valid arguments

    Given: A `_Point` class from the `tally_counter` module.
    When: A `_Point` object is created with keyword arguments
    Then: A object attribute values are set
    """
    from tally_counter.point import _Point

    point = _Point(value=1010, timestamp=1000)

    assert point.value == 1010
    assert point.timestamp == 1000


def test_data():
    from tally_counter.point import _Point

    assert _Point(100, 10000).data == (100, 10000)
