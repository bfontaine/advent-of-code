import pytest

from aoc import assert_examples
import day02
from day02 import Game, ColorSelection


@pytest.mark.parametrize("line,expected", [
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
     Game(n=1, records=[
         ColorSelection(blue=3, red=4),
         ColorSelection(red=1, green=2, blue=6),
         ColorSelection(green=2),
     ])),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
     Game(n=3, records=[
         ColorSelection(green=8, blue=6, red=20),
         ColorSelection(blue=5, red=4, green=13),
         ColorSelection(green=5, red=1),
     ])),
])
def test_game_from_string(line, expected):
    assert Game.from_string(line) == expected


def test_problem1_examples():
    assert_examples(day02.problem1)


def test_problem2_examples():
    assert_examples(day02.problem2)
