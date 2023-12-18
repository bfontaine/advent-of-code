import pytest

from day11 import problem1, problem2, Universe
from aoc import assert_examples


@pytest.mark.parametrize("before", [
    [[True]],
    [[True]] * 2,
    [[True] * 2],
    [[True] * 2] * 2,
    [[True, False], [False, True]],
    [[True, False], [True, True]],
    [[False, True], [False, True], [True, False]],
])
def test_expand_no_change(before):
    universe = Universe(rows=list(before))
    universe.expand()
    assert universe.rows == before


@pytest.mark.parametrize("before,expected", [
    # 1x1 -> 2x2
    ([[False]], [[False] * 2] * 2),
    # 1x2 -> 2x4
    ([[False],
      [False]], [[False, False]] * 4),
    # 2x1 -> 4x2
    ([[False, False]], [[False] * 4] * 2),

    # 2x2 -> 4x4
    ([[False, False],
      [False, False]], [[False] * 4] * 4),

    ([[False, False, True], [True, False, True]],
     [[False, False, False, True], [True, False, False, True]]),
])
def test_expand(before, expected):
    universe = Universe(rows=before)
    universe.expand()
    assert universe.rows == expected


def test_problem1_examples():
    assert_examples(problem1)

# def test_problem2_examples():
#     assert_examples(problem2)
