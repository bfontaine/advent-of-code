import pytest

from aoc.space import NORTH, SOUTH, EAST, WEST


@pytest.mark.parametrize("direction,opposite", [
    (NORTH, SOUTH),
    (WEST, EAST),
])
def test_direction_opposite(direction, opposite):
    assert direction.opposite() == opposite
    assert opposite.opposite() == direction


@pytest.mark.parametrize("direction,force,expected", [
    (NORTH, 1, (0, -1)),
    (NORTH, 2, (0, -2)),
    (EAST, 5, (5, 0)),
])
def test_direction_apply(direction, force, expected):
    assert direction.apply(0, 0, force=force) == expected
