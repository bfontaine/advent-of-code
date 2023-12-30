import enum
from collections import deque
from typing import Set, List

import aoc
from aoc.containers import Grid
from aoc.directions import Direction, EAST, SOUTH, NORTH, WEST


class Tile(str, enum.Enum):
    EMPTY = "."
    SW_NE_MIRROR = "/"
    SE_NW_MIRROR = "\\"
    VERTICAL_SPLITTER = "|"
    HORIZONTAL_SPLITTER = "-"

    def get_new_directions(self, direction: Direction) -> Set[Direction]:
        match self:
            case Tile.EMPTY:
                return {direction, }

            case Tile.SW_NE_MIRROR:
                return {
                    {
                        NORTH: EAST,
                        EAST: NORTH,
                        SOUTH: WEST,
                        WEST: SOUTH,
                    }[direction],
                }

            case Tile.SE_NW_MIRROR:
                return {
                    {
                        NORTH: WEST,
                        EAST: SOUTH,
                        SOUTH: EAST,
                        WEST: NORTH,
                    }[direction],
                }

            case Tile.VERTICAL_SPLITTER:
                splitter_directions = {NORTH, SOUTH}
                if direction in splitter_directions:
                    return {direction, }
                return splitter_directions

            case Tile.HORIZONTAL_SPLITTER:
                splitter_directions = {WEST, EAST}
                if direction in splitter_directions:
                    return {direction, }
                return splitter_directions


class Contraption(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.beams: List[List[Set[Direction]]] = [
            [set() for _ in row]
            for row in self.rows
        ]

    def propagate_beam(self, x: int, y: int, direction: Direction):
        propagation_queue = deque([(x, y, direction)])

        while propagation_queue:
            x1, y1, direction = propagation_queue.popleft()
            x, y = direction.apply(x1, y1)
            if not self.valid_coordinates(x, y):
                continue

            tile = Tile(self.rows[y][x])
            tile_beams = self.beams[y][x]

            directions = tile.get_new_directions(direction)

            for direction in directions:
                if direction not in tile_beams:
                    tile_beams.add(direction)
                    propagation_queue.append((x, y, direction))


def problem1(text: str):
    grid = Contraption.from_string(text)
    grid.propagate_beam(-1, 0, EAST)

    return sum([1 for x, y in grid.iter_chars() if grid.beams[y][x]])


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
