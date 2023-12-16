import pytest

from day10 import problem1, problem2, Position, Map, STARTING_TILE, GROUND
from aoc import assert_examples


@pytest.fixture()
def simple_sample1():
    return """
.....
.S-7.
.|.|.
.L-J.
.....
    """.strip()


def test_tile_equality():
    assert GROUND != STARTING_TILE


def test_position_equality():
    assert Position(10, 34) == Position(10, 34)


def test_starting_position(simple_sample1):
    m = Map.from_text(simple_sample1)
    assert m.starting_position == Position(1, 1)


def test_problem1_examples():
    assert_examples(problem1)

# def test_problem2_examples():
#     assert_examples(problem2)
