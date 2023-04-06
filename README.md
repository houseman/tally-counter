# tally-counter
A Python tally counter class

<p align="center">
![Supported Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![Code Style](https://img.shields.io/badge/style-black-brightgreen)
![Linting](https://img.shields.io/badge/linting-flake8%20%7C%20isort%20%7C%20mypy-yellowgreen)
</p>

## Usage
```python
>>> from tally_counter import Counter

>>> counter = Counter(all=0, odds=0, evens=0)
>>> for x in range(1, 101):  # 1..100 inclusive
...     counter.all += x
...     if x % 2:
...         counter.evens += x
...     else:
...         counter.odds += x
>>> counter.all  # Sum of all natural numbers 1..100
5050.0
>>> counter.evens  # Sum of all even numbers in range 1..100
2500.0
>>> counter.odds  # Sum of all odd numbers in range 1..100
2550.0
>>> counter.all.average()  # Average of all natural numbers 1..100
50.0
>>> counter.evens.average()  # Average of all even numbers in range 1..100
49.01960784313726
>>> counter.odds.average()  # Average of all odd numbers in range 1..100
50.0

```

### Timing
#### Data series age
This is the time difference (in nanoseconds), between the current system time and the time that the first data point in the series was created.

```python
>>> counter.all.age()
507500

```

#### Data series time span
This is the time difference (in nanoseconds), between the first and the latest data points' timestamps.

```python
>>> counter.evens.span()
495000

```

### Setting a TTL for counters
It is possible to set a TTL (Time-To-Live) for a counter, through setting a `ttl` argument value in milliseconds.
If this is set, then counters that exceed that TTL in age are discarded.
This may be useful for things such as rate limits (a use case where counts should be made irrelevant once a certain amount of time has passed).

```python
>>> r_counter = Counter(requests=0, ttl=60000)  # Count requests for the past minute

```
