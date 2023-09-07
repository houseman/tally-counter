"""`Counter` unit tests."""
import threading

import pytest


def test_init_kwargs():
    from tally_counter import Counter

    counter = Counter(foo=100)
    assert counter.foo == 100


def test_init_args():
    from tally_counter import Counter

    counter = Counter("bar", "baz")
    assert counter.bar == 0
    assert counter.baz == 0


def test_constructor_given_no_attr():
    from tally_counter import Counter

    counter = Counter()
    assert counter.dump() == {}


def test_ttl_attr():
    from tally_counter import Counter

    assert Counter(ttl=3600).ttl == 3600

    assert Counter().ttl is None


def test_invalid_ttl_attr():
    from tally_counter import Counter

    with pytest.raises(TypeError, match="'int' expected for argument 'ttl'"):
        Counter(foo=1001, ttl="foo")


def test_invalid_attr():
    from tally_counter import Counter

    with pytest.raises(ValueError):
        Counter(foo="bar")


def test_init_has_kwargs():
    from tally_counter import Counter

    counter = Counter(foo=100, bar=110)

    assert counter.foo == 100
    assert counter.bar == 110


def test_init_no_kwargs():
    from tally_counter import Counter

    counter = Counter()

    # Attribute does not exist, instantiated to a zero value
    assert counter.foo == 0
    assert counter["oof"] == 0

    # Attribute does not exist, instantiated to a zero value, then incremented
    counter.bar.incr()
    assert counter.bar == 1
    counter["rab"].incr()
    assert counter["rab"] == 1

    # Attribute does not exist, instantiated to a zero value, then incremented by a
    # given value
    counter.baz.incr(1234)
    assert counter.baz == 1234
    counter["zab"].incr(1234)
    assert counter["zab"] == 1234


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


def test_dump():
    from tally_counter import Counter

    counter = Counter("foo")
    counter.foo.incr(1022, timestamp=1000)
    counter.foo.incr(1023, timestamp=1001)
    counter.foo.incr(1024, timestamp=1002)

    assert counter.dump() == {"foo": [(1022, 1000), (1023, 1001), (1024, 1002)]}


@pytest.fixture()
def patch_time(mocker):
    ...


def test_thread_safety(patch_time):
    from tally_counter import Counter

    # Define a function that will be executed by each thread
    def thread_function(counter: Counter, fr: int, to: int):
        for _ in range(fr, to + 1):
            counter.cnt.incr()

    counter = Counter(cnt=0)

    # Create two threads that will access the shared instance
    thread_1 = threading.Thread(
        target=thread_function, kwargs={"counter": counter, "fr": 1, "to": 10000}
    )
    thread_2 = threading.Thread(
        target=thread_function, kwargs={"counter": counter, "fr": 10001, "to": 20000}
    )
    thread_3 = threading.Thread(
        target=thread_function, kwargs={"counter": counter, "fr": 20001, "to": 30000}
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

    # Check if the shared property has the expected value
    assert counter.cnt.len() == 230001
