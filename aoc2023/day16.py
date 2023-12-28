import enum
import time
from collections import deque
from typing import Set, List

from colorama import Back

import aoc
from aoc import c
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
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.beams: List[List[Set[Direction]]] = [
            [set() for _ in row]
            for row in self.rows
        ]

    def propagate_beams(self, visual=False):
        propagation_queue = deque([(-1, 0, EAST)])

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

                if visual:
                    print("\033[H\033[J", end="")
                    print(self.pretty_string())
                    time.sleep(0.2)

    def pretty_string(self) -> str:
        rows: List[str] = []
        for y, row in enumerate(self.rows):
            row_parts: List[str] = []
            for x, tile in enumerate(row):
                beams = len(self.beams[y][x])
                color = [Back.WHITE, Back.YELLOW, Back.RED, Back.MAGENTA, Back.BLUE][beams]
                row_parts.append(c(tile, color))

            rows.append("".join(row_parts))
        return "\n".join(rows)


def problem1(text: str, visual=False):
    grid = Contraption.from_string(text)
    grid.propagate_beams(visual=visual)

    return sum([1 for x, y in grid.iter_chars() if grid.beams[y][x]])


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2, flags=["visual"])
