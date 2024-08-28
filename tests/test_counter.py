"""`Counter` unit tests."""

import re
import threading

import pytest


def test_init__with_kwargs():
    """
    Test the initialization of a `Counter` object with keyword arguments.

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with the keyword argument "foo" set to 100.
    Then: The "foo" attribute of the Counter object should be equal to 100.
    """
    from tally_counter import Counter

    counter = Counter(foo=100)

    assert counter.foo == 100


def test_init__with_args():
    """
    Test the initialization of a `Counter` object with positional arguments.

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with the positional argument "foo".
    Then: The "foo" attribute of the Counter object should be equal to 0.
    """
    from tally_counter import Counter

    counter = Counter("bar")

    assert counter.bar == 0


def test_init__no_args_or_kwargs():
    """
    Test the initialization of a `Counter` object with no arguments.

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with no positional or keyword arguments
    Then: The object should contain no data
    """
    from tally_counter import Counter

    counter = Counter()

    assert counter.data == {}


def test_init__valid_ttl_kwarg():
    """
    Test the initialization of a `Counter` object with a valid `ttl` keyword argument.

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with a `ttl` keyword argument set to 3600
    Then: The object `ttl` attribute value should be 3600
    """
    from tally_counter import Counter

    assert Counter(ttl=3600).ttl == 3600


def test_init__invalid_ttl_kwarg():
    """
    Test the initialization of a `Counter` object with an invalid `ttl` keyword argument

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with a `ttl` keyword argument set to "foo"
    Then: A `TypeError` exception should raise
    """
    from tally_counter import Counter

    with pytest.raises(TypeError, match="'int' expected for argument 'ttl'"):
        Counter(foo=1001, ttl="foo")


def test_init__invalid_kwarg_value():
    """
    Test the initialization of a `Counter` object with an invalid keyword argument

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with a `foo` keyword argument set to "bar"
    Then: A `ValueError` exception should raise
    """
    from tally_counter import Counter

    with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 10: 'bar'")):
        Counter(foo="bar")


def test_init__valid_kwarg_value():
    """
    Test the initialization of a `Counter` object with a valid keyword argument

    Given: A `Counter` class from the `tally_counter` module.
    When: A `Counter` object is created with a `foo` keyword argument set to 100
    Then: A object "foo" attribute value is equal to 100
    """
    from tally_counter import Counter

    counter = Counter(foo=100)

    assert counter.foo == 100
    assert counter["foo"] == 100


def test_get__create_if_not_defined():
    """
    Test the auto-creation of a `Counter` object attribute

    Given: A `Counter` class from the `tally_counter` module
    When: No attribute exists for the given key
    Then: Create an empty series and return that
    """
    from tally_counter import Counter

    counter = Counter()

    assert counter.foo == 0
    assert counter["oof"] == 0


@pytest.mark.parametrize("kwargs", [{"all": 0, "odds": 0, "evens": 0}, {}])
def test_through(kwargs):
    from tally_counter import Counter

    counter = Counter(**kwargs)
    for x in range(1, 101):  # Including 1, 100
        counter.all.incr(x)
        if x % 2:
            counter.evens.incr(x)  # Add to "evens" counter
        else:
            counter.odds.incr(x)  # Add to "odds" counter

    assert counter.all == 5050  # Sum of natural numbers 1 to 100
    assert counter["all"] == 5050
    assert counter.evens == 2500
    assert counter["evens"] == 2500
    assert counter.odds == 2550
    assert counter["odds"] == 2550


def test_data():
    from tally_counter import Counter

    counter = Counter("foo")
    counter.foo.incr(1022, timestamp=1000)
    counter.foo.incr(1023, timestamp=1001)
    counter.foo.incr(1024, timestamp=1002)

    assert counter.data == {"foo": [(1022, 1000), (1023, 1001), (1024, 1002)]}


@pytest.fixture
def patch_time(mocker): ...


def test_thread_safety(patch_time):  # noqa: ARG001
    from tally_counter import Counter

    # Define a function that will be executed by each thread
    def thread_function(counter: Counter, fr: int, to: int):
        for _ in range(fr, to + 1):
            counter.cnt.incr()

    counter = Counter(cnt=0)

    # Create three threads that will access the shared instance
    thread_1 = threading.Thread(target=thread_function, kwargs={"counter": counter, "fr": 1, "to": 10000})
    thread_2 = threading.Thread(
        target=thread_function,
        kwargs={"counter": counter, "fr": 10001, "to": 20000},
    )
    thread_3 = threading.Thread(
        target=thread_function,
        kwargs={"counter": counter, "fr": 20001, "to": 30000},
    )

    # Start the threads
    thread_1.start()
    thread_2.start()
    thread_3.start()

    # Wait for both threads to complete
    thread_1.join()
    thread_2.join()
    thread_3.join()

    thread_function(counter=counter, fr=1, to=200000)

    # Check if the shared instance has the expected length
    assert counter.cnt.len() == 230001
