import pytest

from aoc.directions import NORTH, SOUTH, EAST, WEST


@pytest.mark.parametrize("direction,opposite", [
    (NORTH, SOUTH),
    (WEST, EAST),
])
def test_direction_opposite(direction, opposite):
    assert direction.opposite() == opposite
    assert opposite.opposite() == direction
