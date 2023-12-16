from dataclasses import dataclass, field
from typing import List, Optional

import aoc


@dataclass(frozen=True)
class Direction:
    dx: int
    dy: int


NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)

_OPPOSITE_DIRECTIONS = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST,
}

DIRECTIONS = tuple(_OPPOSITE_DIRECTIONS)


def get_opposite_direction(direction: Direction):
    return _OPPOSITE_DIRECTIONS[direction]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def go_to(self, direction: Direction):
        return Position(x=self.x + direction.dx, y=self.y + direction.dy)


class Tile:
    pass


STARTING_TILE = Tile()
GROUND = Tile()


@dataclass(frozen=True)
class Pipe(Tile):
    symbol: str
    direction1: Direction
    direction2: Direction

    def is_connected(self, direction: Direction):
        return direction == self.direction1 or direction == self.direction2

    def opposite_end(self, direction: Direction):
        if direction == self.direction1:
            return self.direction2
        if direction == self.direction2:
            return self.direction1
        raise ValueError(f"Pipe {self} is not connected to {direction}")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.symbol})"


def parse_tile(sym: str) -> Tile:
    match sym:
        case '|':
            return Pipe(sym, NORTH, SOUTH)
        case '-':
            return Pipe(sym, WEST, EAST)
        case 'L':
            return Pipe(sym, NORTH, EAST)
        case 'J':
            return Pipe(sym, NORTH, WEST)
        case '7':
            return Pipe(sym, SOUTH, WEST)
        case 'F':
            return Pipe(sym, SOUTH, EAST)
        case 'S':
            return STARTING_TILE
        case '.':
            return GROUND
        case _:
            raise ValueError(f"Unrecognized symbol {sym}")


@dataclass
class Map:
    tiles: List[List[Tile]] = field(default_factory=list)
    _starting_position: Optional[Position] = None

    @classmethod
    def from_text(cls, text: str):
        m = cls()
        for line in text.splitlines(keepends=False):
            m.tiles.append([parse_tile(c) for c in line])
        return m

    @property
    def starting_position(self):
        if self._starting_position is None:
            for y, row in enumerate(self.tiles):
                for x, tile in enumerate(row):
                    if tile == STARTING_TILE:
                        self._starting_position = Position(x, y)
                        return self._starting_position
            raise RuntimeError("Can't find starting position")
        return self._starting_position

    def get(self, position: Position):
        try:
            return self.tiles[position.y][position.x]
        except IndexError:
            return None

    def get_connected_pipe(self, origin: Position, direction: Direction):
        """
        Look for a tile going from ``origin`` to ``direction``, and if there is a pipe there that’s connected to
        ``origin``, return a tuple of ``(new_position, next_direction)`` where ``new_position`` is the position of the
        pipe tile and ``next_direction`` is the next direction to use to follow the pipe.
        """
        new_position = origin.go_to(direction)
        pipe = self.get(new_position)
        if not isinstance(pipe, Pipe):
            return None

        direction_to_origin = get_opposite_direction(direction)

        if pipe.is_connected(direction_to_origin):
            return new_position, pipe.opposite_end(direction_to_origin)

        return None

    def get_initial_pipe(self) -> tuple[Position, Direction]:
        for direction in DIRECTIONS:
            if initial_pipe := self.get_connected_pipe(self.starting_position, direction):
                return initial_pipe
        raise RuntimeError("Can't find initial pipe")


def problem1(text: str):
    m = Map.from_text(text)
    initial_position = m.starting_position

    new_position, next_direction = m.get_initial_pipe()
    steps = 1
    while new_position != initial_position:
        next_pipe = m.get_connected_pipe(new_position, next_direction)
        steps += 1
        if next_pipe is None:
            assert new_position.go_to(next_direction) == initial_position
            break

        new_position, next_direction = next_pipe

    return steps // 2


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
