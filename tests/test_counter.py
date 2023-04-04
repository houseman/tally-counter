def test_init():
    from tally_counter import Counter

    assert Counter() is not None


def test_init_kwargs():
    from tally_counter import Counter

    counter = Counter(foo=100.0, bar=110)

    assert counter.foo == 100
    assert counter.foo == 100.0
    assert counter.bar == 110.0
    assert counter.bar == 110
