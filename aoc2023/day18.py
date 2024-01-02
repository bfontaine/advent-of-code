import enum
from collections import deque
from typing import Set, Tuple, List, Deque

import aoc
from aoc.space import Position, Direction

"""
Note: the problem is underspecified but we assume there aren’t weird things in the dig plans
  like overlaps ("8" shapes), dead ends ("U 5" followed by "D 5"), etc.
"""


class Tile(str, enum.Enum):
    GROUND = "."
    DUG = "#"


class Terrain:
    def __init__(self):
        self.dug_tiles: Set[Position] = set()
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

    def dig(self, p: Position):
        self.min_x = min(self.min_x, p.x)
        self.max_x = max(self.max_x, p.x)
        self.min_y = min(self.min_y, p.y)
        self.max_y = max(self.max_y, p.y)

        self.dug_tiles.add(p)

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

    def pretty_print(self):
        for y in self.range_y:
            row = [self.get(Position(x, y)) for x in self.range_x]
            print("".join(row))


def parse_dig_plan(text: str):
    instructions: List[Tuple[Direction, int, str]] = []

    for line in text.splitlines():
        direction_str, amount, _ = line.split()
        instructions.append((
            Direction.from_char(direction_str),
            int(amount),
            ""  # useless in part 1
        ))

    return instructions


def problem1(text: str):
    dig_plan = parse_dig_plan(text)
    terrain = Terrain()
    position = Position(0, 0)
    terrain.dig(position)
    for direction, amount, _ in dig_plan:
        for _ in range(amount):
            position = position.go_to(direction)
            terrain.dig(position)

    # terrain.pretty_print()

    outside_tiles = terrain.get_outside_tiles_count()
    total_size = terrain.height * terrain.width

    return total_size - outside_tiles


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
