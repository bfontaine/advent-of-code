import pytest

import day01
from aoc import assert_examples


def test_problem1_examples():
    assert_examples(day=1, problem=1, fn=lambda s: day01.problem(1, s),
                    examples={0,})


@pytest.mark.parametrize("line,p,expected", [
    ("23", 1, 23),
    ("23", 2, 23),
    ("1two", 1, 11),
    ("1two", 2, 12),
    ("twone", 2, 21),
])
def test_get_line_calibration_value(line, p, expected):
    assert day01.get_line_calibration_value(line, p=p) == expected
