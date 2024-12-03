import argparse
import re
import traceback
import warnings
from collections.abc import Iterable
from datetime import date
from os import environ
from typing import Any, Callable

import aocd
from aocd.models import Puzzle
from dotenv import load_dotenv

from .display import colored_text, c

__all__ = [
    "get_input_data", "run",
    "get_puzzle",
    "refresh_examples",
    "assert_examples",
    "colored_text", "c",
]

load_dotenv()

YEAR = int(environ.get("AOC_YEAR") or date.today().year)

Solution = Callable[[str], Any]


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


def get_puzzle(day: int | None = None):
    if day is None:
        day = get_day()

    return Puzzle(year=YEAR, day=day)


def get_input_data():
    day, year = get_day_and_year()
    return aocd.get_data(day=day, year=year)


def example_input_data(day: int | None = None) -> str:
    """Get the first example's input data."""
    puzzle = get_puzzle(day=day)
    assert puzzle.examples, "Puzzle must have examples"
    return puzzle.examples[0].input_data


def refresh_examples():
    # https://github.com/wimglenn/advent-of-code-data/issues/133#issuecomment-1848840478
    puzzle = get_puzzle()
    puzzle.prose0_path.unlink(missing_ok=True)


def assert_examples(fn: Solution,
                    problem: int | None = None,
                    examples: Iterable[int] | None = None):
    if problem is None:
        if match := re.match(r"problem(\d+)", fn.__name__):
            problem = int(match.group(1))
        else:
            raise ValueError(f"Can't determine problem number from {fn.__name__}")

    assert problem in {1, 2}

    example_indexes: set[int] = set(examples) if examples else set()

    puzzle = get_puzzle()
    for i, example in enumerate(puzzle.examples):
        if example_indexes and i not in example_indexes:
            continue

        expected_response = example.answers[problem - 1]
        if expected_response is None:
            warnings.warn(f"Problem #{problem}, sample #{i + 1}: expected response is None")
            continue

        actual_response = str(fn(example.input_data))
        assert actual_response == expected_response, \
            f"Problem #{problem}, sample #{i + 1}: expected {expected_response}, got {actual_response}"


def run(
        solution1: Solution,
        solution2: Solution | None = None,
        *,
        flags: list[str] | None = None,
):
    p = argparse.ArgumentParser()
    p.add_argument("--refresh-examples", "-r", action="store_true",
                   help="Invalidate the cache used for the examples and exit.")
    p.add_argument("problem", type=int, nargs="?", choices=(1, 2), metavar="PROBLEM",
                   help="Run only the specified problem.")

    if flags is None:
        flags = []

    for flag in flags:
        p.add_argument(f"--{flag}", action="store_true")

    opts = p.parse_args()
    kwargs = {flag: getattr(opts, flag) for flag in flags}

    problem = opts.problem

    if opts.refresh_examples:
        refresh_examples()
        return

    input_data = get_input_data()

    if not problem or problem == 1:
        # noinspection PyArgumentList
        print("Problem #1:", solution1(input_data, **kwargs))

    if not solution2:
        if problem == 2:
            raise RuntimeError("Solution 2 is not implemented")

        return

    if not problem or problem == 2:
        # noinspection PyArgumentList
        print("Problem #2:", solution2(input_data, **kwargs))
