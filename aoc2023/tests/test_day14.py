import pytest

from aoc import assert_examples
from day14 import problem1, problem2, roll_column


@pytest.mark.parametrize("rolled,column", [
    ("###", "###"),
    ("OOO", "OOO"),
    ("...", "..."),
    ("O..", "O.."),
    ("O..", ".O."),
    ("O..", "..O"),
    ("OO.", "OO."),
    ("OO.", "O.O"),
    ("OO.", ".OO"),
    (".#OO...#O#O..#O..",
     ".#..O.O#O#.O.#..O"),
])
def test_roll_column(rolled, column):
    assert roll_column(column) == rolled


def test_problem1_examples():
    assert_examples(problem1)


def test_problem2_examples():
    assert_examples(problem2)
