import pytest

from aoc import assert_examples
from day18 import problem1, problem2


def test_problem1_empty():
    assert problem1("") == 1


@pytest.mark.parametrize("square_size", list(range(1, 40)))
def test_problem1_squares(square_size):
    plan = "\n".join([f"{direction} {square_size} (#000000)"
                      for direction in "URDL"])

    assert problem1(plan) == (square_size + 1) ** 2


@pytest.mark.parametrize("size", list(range(2, 40)))
def test_problem1_l(size):
    # L
    plan = (
        f"D {size} (#000000)\n"
        f"R {size} (#000000)\n"
        "U 1 (#000000)\n"
        f"L {size - 1} (#000000)\n"
        f"U {size - 1} (#000000)\n"
        "L 1 (#000000)"
    )

    assert problem1(plan) == (size + 1) ** 2 - (size - 1) ** 2


def test_problem1():
    # Mypy rejects string unpacking although it’s perfectly valid Python code
    # https://github.com/python/mypy/issues/13823
    plan = "\n".join([  # type: ignore
        f"{direction} {amount} (#000000)"  # type: ignore
        for direction, amount in ("D1", "R1", "U2", "L3", "D1", "R1")
    ])
    assert problem1(plan) == 10


def test_problem1_examples():
    assert_examples(problem1)


def test_problem2_examples():
    assert_examples(problem2)
