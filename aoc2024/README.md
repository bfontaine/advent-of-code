# Advent of code 2024

This setup is the same as [last year](../aoc2023).

## Setup

    poetry install

### Config

```
AOC_SESSION=...
AOC_YEAR=2024
```

## Run

    poetry run python dayXX.py [1|2]

## Tests

    poetry run mypy day*.py
    poetry run pytest
