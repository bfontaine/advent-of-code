from datetime import date
from os import environ
from typing import Any, Callable, Set, Optional, Iterable

from dotenv import load_dotenv
from aocd.models import Puzzle

__all__ = [
    "YEAR",
    "Puzzle",
    "get_input_data", "assert_examples",
]

load_dotenv()

YEAR: str = environ.get("AOC_YEAR") or str(date.today().year)


def get_input_data(day: int):
    return Puzzle(year=YEAR, day=day).input_data


def assert_examples(day: int, problem: int, fn: Callable[[str], Any],
                    examples: Optional[Iterable[int]] = None):
    assert problem in {1, 2}

    example_indexes: Set[int] = set(examples) if examples else set()

    puzzle = Puzzle(year=YEAR, day=day)
    for i, example in enumerate(puzzle.examples):
        if example_indexes and i not in example_indexes:
            continue

        expected_response = example.answers[problem - 1]
        actual_response = str(fn(example.input_data))
        assert actual_response == expected_response, \
            f"Sample #{i + 1}: expected {expected_response}, got {actual_response}"
