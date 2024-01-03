import enum
from collections import deque
from typing import Set, Tuple, Deque, Iterator

import aoc
from aoc.space import Position, Direction, SOUTH, EAST, WEST, NORTH


class Tile(str, enum.Enum):
    GROUND = "."
    DUG = "#"


class Terrain:
    def __init__(self):
        self.dug_tiles: Set[Position] = set()
        self.current_position = Position(0, 0)
        self.min_x = self.max_x = self.min_y = self.max_y = 0

    @property
    def width(self):
        return self.max_x - self.min_x + 1

    @property
    def height(self):
        return self.max_y - self.min_y + 1

    @property
    def range_x(self):
        return range(self.min_x, self.max_x + 1)

    @property
    def range_y(self):
        return range(self.min_y, self.max_y + 1)

    def valid_position(self, pos: Position):
        return self.min_x <= pos.x <= self.max_x and self.min_y <= pos.y <= self.max_y

    def get(self, p: Position):
        if p in self.dug_tiles:
            return Tile.DUG
        return Tile.GROUND

    def dig(self):
        p = self.current_position
        self.min_x = min(self.min_x, p.x)
        self.max_x = max(self.max_x, p.x)
        self.min_y = min(self.min_y, p.y)
        self.max_y = max(self.max_y, p.y)

        self.dug_tiles.add(p)

    def dig_trench(self, direction: Direction, amount: int):
        # TODO store ranges
        #   - {y: range(x1, x2)} for horizontal ranges
        #   - {x: range(y1, y2)} for vertical ranges
        #  => ok but we won't count outside tiles one by one
        for _ in range(amount):
            self.dig()
            self.current_position = self.current_position.go_to(direction)
            self.dig()

    def get_outside_tiles_count(self):
        outside_tiles = 0
        seen: Set[Position] = set()
        queue: Deque[Position] = deque()

        # start from the edges
        for y in self.range_y:
            # left
            queue.append(Position(x=self.min_x, y=y))
            # right
            queue.append(Position(x=self.max_x, y=y))

        for x in self.range_x:
            # top
            queue.append(Position(x=x, y=self.min_y))
            # bottom
            queue.append(Position(x=x, y=self.max_y))

        while queue:
            pos = queue.popleft()

            if pos in seen:
                continue

            seen.add(pos)

            if self.get(pos) == Tile.DUG or not self.valid_position(pos):
                continue

            outside_tiles += 1

            for neighbor in pos.iter_neighbors():
                if neighbor in seen or not self.valid_position(neighbor):
                    continue

                queue.append(neighbor)

        return outside_tiles

    def get_dug_tiles_count(self):
        outside_tiles = self.get_outside_tiles_count()
        total_size = self.height * self.width

        return total_size - outside_tiles

    def pretty_print(self):
        for y in self.range_y:
            row = [self.get(Position(x, y)) for x in self.range_x]
            print("".join(row))


def parse_dig_plan(text: str, mode: int) -> Iterator[Tuple[Direction, int]]:
    assert mode in {1, 2}

    for line in text.splitlines():
        if mode == 1:
            direction_str, amount_str, _ = line.split()
        else:
            color_code = line.rstrip(")").split("#", 1)[1]
            # > The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.
            direction_str = "RDLU"[int(color_code[-1])]
            amount_str = color_code[:-1]

        yield (
            Direction.from_char(direction_str),
            int(amount_str),
        )


def run(text: str, mode: int):
    position = Position(0, 0)
    x2 = y2 = 0

    # https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula
    double_area = 0
    parse_dig_plan(text, mode=mode)

    for direction, amount in parse_dig_plan(text, mode=mode):
        x1 = x2
        y1 = y2

        position = position.go_to(direction, amount)
        x2 = position.x
        y2 = position.y

        double_area += (y1 + y2) * (x1 - x2)

    return int(abs(double_area / 2))


def problem1(text: str):
    return run(text, mode=1)


def problem2(text: str):
    return run(text, mode=2)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
