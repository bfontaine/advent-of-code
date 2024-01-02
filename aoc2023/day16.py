import enum
from collections import deque
from typing import Set, List, Tuple, Iterator

import aoc
from aoc.containers import StringGrid
from aoc.space import Direction, EAST, SOUTH, NORTH, WEST


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


class Contraption(StringGrid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.beams: List[List[Set[Direction]]] = []
        self.reset_beams()

    def reset_beams(self):
        self.beams = [
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

    def count_energized_tiles(self):
        return sum(1 for x, y in self.iter_coordinates() if self.beams[y][x])


def problem1(text: str):
    grid = Contraption.from_string(text)
    grid.propagate_beam(-1, 0, EAST)

    return grid.count_energized_tiles()


def gen_all_beams(grid: Contraption) -> Iterator[Tuple[int, int, Direction]]:
    for y in range(grid.height):
        yield -1, y, EAST  # from left
        yield grid.width, y, WEST  # from right

    for x in range(grid.width):
        yield x, -1, SOUTH  # from top
        yield x, grid.height, NORTH  # from bottom


def problem2(text: str):
    grid = Contraption.from_string(text)
    max_energized_tiles = 0

    beam: Tuple[int, int, Direction]
    for beam in gen_all_beams(grid):
        grid.propagate_beam(*beam)
        max_energized_tiles = max(
            max_energized_tiles,
            grid.count_energized_tiles(),
        )
        grid.reset_beams()

    return max_energized_tiles


if __name__ == '__main__':
    aoc.run(problem1, problem2)
