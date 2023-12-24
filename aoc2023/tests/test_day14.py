import pytest

from aoc import assert_examples, get_input_data
from day14 import problem1, problem2, _roll_line, Support


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
    assert _roll_line(column) == rolled


def test_problem1_examples():
    assert_examples(problem1)


def test_problem1_input():
    assert problem1(get_input_data()) == 110821


def test_roll_north_south():
    text = get_input_data()
    support = Support.from_string(text)
    north_south = support.copy().roll_north().roll_south()
    south = support.copy().roll_south()
    assert north_south == south

    south_north_south = support.copy().roll_south().roll_north().roll_south()
    assert south_north_south == south


def test_problem2_examples():
    assert_examples(problem2)
