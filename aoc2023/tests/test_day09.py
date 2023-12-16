import pytest

from day09 import problem1, problem2, differences, differences_sequences, extrapolate, extrapolate_backward
from aoc import assert_examples


def test_differences():
    assert differences([1, 2]) == [1]
    assert differences([0, 3, 6, 9]) == [3, 3, 3]
    assert differences([3] * 20) == [0] * 19


def test_differences_sequences():
    assert differences_sequences([0, 3, 6, 9, 12, 15]) == \
           [
               [0, 3, 6, 9, 12, 15],
               [3, 3, 3, 3, 3],
               [0, 0, 0, 0],
           ]


def test_extrapolate():
    assert extrapolate([0, 1, 2, 3]) == 4
    assert extrapolate([0, 1, 3, 6, 10]) == 15


@pytest.mark.parametrize("it,expected", [
    (range(20), -1),
    (range(100), -1),
    ([3, 6, 9], 0),
    ([20, 30, 40], 10),
])
def test_extrapolate_backward(it, expected):
    assert extrapolate_backward(list(it)) == expected


def test_problem1_examples():
    assert_examples(problem1)


def test_problem2_examples():
    assert_examples(problem2)
