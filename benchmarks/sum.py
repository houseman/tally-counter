import numpy as np

from tally_counter import Counter

RANGE = (1, 10000)
NUMBER = 100


def run_tally() -> None:
    counter = Counter("benchmark")
    for i in range(RANGE[0], RANGE[1]):
        counter.benchmark.incr(i, timestamp=1)

    _ = counter.benchmark.sum()
    _ = counter.benchmark.mean()


def run_naive() -> None:
    _ = np.sum(range(RANGE[0], RANGE[1]))
    _ = np.mean(range(RANGE[0], RANGE[1]))


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(run_tally, number=NUMBER) / NUMBER)
    print(timeit.timeit(run_naive, number=NUMBER) / NUMBER)
