import re
import traceback
from datetime import date
from os import environ
from typing import Any, Callable, Set, Optional, Iterable

from dotenv import load_dotenv
import aocd
from aocd.models import Puzzle

__all__ = [
    "get_input_data", "assert_examples", "run",
]

load_dotenv()

YEAR = int(environ.get("AOC_YEAR") or date.today().year)


def get_day():
    # Simplified implementation of aocd.get_day_and_year()
    # https://github.com/wimglenn/advent-of-code-data/blob/34d73e3f/aocd/get.py#L106
    day_re = re.compile(r".*day(\d+)\.py")

    for frame in traceback.extract_stack():
        filename = frame[0]
        if match := day_re.match(filename):
            return int(match.group(1))

    raise ValueError("Can't determine day")


def get_day_and_year():
    return get_day(), YEAR


def get_input_data():
    day, year = get_day_and_year()
    return aocd.get_data(day=day, year=year)


def assert_examples(fn: Callable[[str], Any],
                    problem: Optional[int] = None,
                    examples: Optional[Iterable[int]] = None):
    if problem is None:
        if match := re.match(r"problem(\d+)", fn.__name__):
            problem = int(match.group(1))
        else:
            raise ValueError(f"Can't determine problem number from {fn.__name__}")

    assert problem in {1, 2}

    example_indexes: Set[int] = set(examples) if examples else set()

    day, year = get_day_and_year()
    puzzle = Puzzle(year=year, day=day)
    for i, example in enumerate(puzzle.examples):
        if example_indexes and i not in example_indexes:
            continue

        expected_response = example.answers[problem - 1]
        actual_response = str(fn(example.input_data))
        assert actual_response == expected_response, \
            f"Sample #{i + 1}: expected {expected_response}, got {actual_response}"


def run(fn: Callable[[str], Any]):
    print(fn(get_input_data()))
