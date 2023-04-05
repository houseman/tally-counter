import pytest


def test_init():
    from tally_counter import Counter

    counter = Counter(foo=100)
    assert counter.foo == 100


def test_at_least_one_attr():
    from tally_counter import Counter

    with pytest.raises(TypeError, match="Counter expects at least 1 attribute"):
        Counter()


def test_no_ttl_attr():
    from tally_counter import Counter

    counter = Counter(foo=1001, ttl=3600)
    with pytest.raises(AttributeError):
        counter.ttl


def test_invalid_ttl_attr():
    from tally_counter import Counter

    with pytest.raises(TypeError):
        Counter(foo=1001, ttl="foo")


def test_invalid_attr():
    from tally_counter import Counter

    with pytest.raises(ValueError):
        Counter(foo="bar")


def test_init_kwargs():
    from tally_counter import Counter

    counter = Counter(foo=100.0, bar=110)

    assert counter.foo == 100
    assert counter.foo == 100.0
    assert counter.bar == 110.0
    assert counter.bar == 110


def test_through():
    from tally_counter import Counter

    counter = Counter(all=0, odds=0, evens=0)
    for x in range(1, 101):  # Including 1, 100
        counter.all += x
        if x % 2:
            counter.evens += x  # Add to "evens" counter
        else:
            counter.odds += x  # Add to "odds" counter

    assert counter.all == 5050  # Sum of natural numbers 1 to 100
    assert counter.evens == 2500
    assert counter.odds == 2550
    assert counter.evens + counter.odds == counter.all
