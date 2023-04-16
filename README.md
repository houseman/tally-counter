# tally-counter
A Python tally counter class

![Supported Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![Code Style](https://img.shields.io/badge/style-black-brightgreen)
![Linting](https://img.shields.io/badge/linting-flake8%20%7C%20isort%20%7C%20mypy-yellowgreen)

## Usage
This contrived sample counts numbers from 1 to 100. We count the following metrics
- an aggregate (sum) of all natural numbers from 1 to 100
- a separate aggregate sum of all even numbers from 1 to 100
- a separate aggregate sum of all odd numbers from 1 to 100
- a count of the numbers from 1 to 100

```python
>>> from tally_counter import Counter

>>> counter = Counter("numbers", "naturals", "odds", "evens")
>>> for x in range(1, 101):  # 1..100 inclusive
...     counter.naturals.incr(x)
...     if x % 2 == 0:
...         counter.evens.incr(x)
...     else:
...         counter.odds.incr(x)
...
...     counter.numbers.incr()  # Default increment value is 1

```

These metrics are now available to us
### Sum of all natural numbers from 1 to 100
```python
>>> counter.naturals
5050

```
### Count of all natural numbers from 1 to 100
```python
>>> counter.numbers
100

```

### Sum of all even numbers in range 1 to 100
```python
>>> counter.evens
2550

```
### Sum of all odd numbers in range 1 to 100
```python
>>> counter.odds
2500

```
### Average of all natural numbers 1 to 100
```python
>>> counter.naturals.average()
50.5

```
### Average of all even numbers in range 1 to 100
```python
>>> counter.evens.average()  # Returns a float type
51.0

```
### Average of all odd numbers in range 1 to 100
```python
>>> counter.odds.average()
50.0

```
### Length (number of data points in) of a data series
```python
>>> counter.numbers.len()
100

```

### Timing
#### Data series age
This is the time difference (in nanoseconds), between the current system time and the time that the first data point in the series was created.

```python
>>> counter.naturals.age()
750000

```

#### Data series time span
This is the time difference (in nanoseconds), between the first and the latest data points' timestamps.

```python
>>> counter.evens.span()
735000

```

### Adding or Subtracting
The `incr()` method should be used to add positive counter values to a data series
```python
>>> my_count = Counter("my")
>>> my_count.my.incr(1000)
>>> my_count.my
1000

```

To decrease a data series, use the `decr()` method
```python
>>> my_count.my.decr(100)
>>> my_count.my
900

```

### Setting a TTL for counters
It is possible to set a TTL (Time-To-Live) for a counter, through setting a `ttl` argument value in milliseconds.
If this is set, then counters that exceed that TTL in age are discarded.
This may be useful for things such as rate limits (a use case where counts should be made irrelevant once a certain amount of time has passed).

```python
>>> r_counter = Counter("requests", ttl=60000)  # Count requests for the past minute

```

### Setting an initial value for counters
It is possible to create the counters and set an initial data point at once
```python
>>> foo_counter = Counter(foo=100, bar=200)
>>> foo_counter.foo.incr(1)
>>> foo_counter.foo
101
>>> foo_counter.bar
200

```

### Counter auto-instantiation
By default, a counter data series will be created if it is accessed but does not yest
exist, and will be set to an initial value of zero.
```python
>>> bar_counter = Counter()
>>> bar_counter.bar
0

```

## Documentation for Contributors
- [Developer Notes](./docs/DEV.md)
