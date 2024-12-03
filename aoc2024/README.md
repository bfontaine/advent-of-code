# Advent of code 2024

This setup is the same as [last year](../aoc2023).

## Setup

    poetry install

### Config

```
AOC_SESSION=...
AOC_YEAR=2024
```

See [here](https://github.com/wimglenn/advent-of-code-wim/issues/1) to get your session key.

## Run

    poetry run python dayXX.py [1|2]

## Tests

    poetry run mypy day*.py
    poetry run pytest
