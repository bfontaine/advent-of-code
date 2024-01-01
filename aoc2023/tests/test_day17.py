import pytest

from aoc import assert_examples, get_input_data
from day17 import problem1, problem2


@pytest.mark.parametrize("text,expected", [
    ("12\n"
     "34", 6),
    ("120\n"
     "341", 3),
    ("000000\n"
     "111110", 2),
    # ("000000\n"
    #  "119100", 3),
])
def test_problem1(text, expected):
    assert problem1(text) == expected


def test_problem1_examples():
    assert_examples(problem1, examples=(0,))


def test_problem2_examples():
    assert_examples(problem2)


def test_problem2_input():
    assert problem2(get_input_data()) > 1144  # "too low"
