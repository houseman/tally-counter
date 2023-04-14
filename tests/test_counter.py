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

    # Attribute does not exist, instantiated to a zero value, then incremented
    counter.bar.incr()
    assert counter.bar == 1

    # Attribute does not exist, instantiated to a zero value, then incremented by a
    # given value
    counter.baz.incr(1234)
    assert counter.baz == 1234


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
    assert counter.evens == 2500
    assert counter.odds == 2550


def test_dump():
    from tally_counter import Counter

    counter = Counter("foo")
    counter.foo.incr(1022, timestamp=1000)
    counter.foo.incr(1023, timestamp=1001)
    counter.foo.incr(1024, timestamp=1002)

    assert counter.dump() == {"foo": [(1022, 1000), (1023, 1001), (1024, 1002)]}
