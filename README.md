# tally-counter
A Python tally counter class

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
>>> counter.all
5050.0
>>> counter.evens
2500.0
>>> counter.odds
2550.0
>>> counter.evens + counter.odds
5050.0
>>> counter.all.average()
50.0
>>> counter.evens.average()
49.509803921568626
>>> counter.odds.average()
50.0

```

## Development
### Setup
#### Install dependencies

```shell
make install-deps
```

#### Update dependencies

```shell
make update-deps
```

### Linting
This target will run the `pre-commit`  hooks.
```shell
 make lint
```
