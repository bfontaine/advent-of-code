import enum
from dataclasses import dataclass
from typing import List, Optional, Set, Iterator, Dict

from colorama import Back, Fore, Style

import aoc
from aoc import c


class Orientation(int, enum.Enum):
    # https://en.wikipedia.org/wiki/Port_and_starboard
    PORTSIDE = enum.auto()
    STARBOARD = enum.auto()


@dataclass(frozen=True)
class Direction:
    dx: int
    dy: int

    def opposite(self):
        return Direction(-self.dx, -self.dy)

    def get_direction_from_orientation(self, orientation: Orientation):
        idx = DIRECTIONS.index(self)
        match orientation:
            case Orientation.PORTSIDE:
                # portside = -90°
                return DIRECTIONS[(idx + len(DIRECTIONS) - 1) % len(DIRECTIONS)]
            case Orientation.STARBOARD:
                # starboard = +90°
                return DIRECTIONS[(idx + 1) % len(DIRECTIONS)]
            case _:
                raise ValueError(f"Invalid orientation {orientation}")

    def __repr__(self):
        return f"{self.__class__.__name__}<{DIRECTION_SYMBOLS[DIRECTIONS.index(self)]}"


NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
DIRECTION_SYMBOLS = "NESW"


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def go_to(self, direction: Direction):
        return Position(x=self.x + direction.dx, y=self.y + direction.dy)

    def iter_neighbors(self):
        return (self.go_to(direction) for direction in DIRECTIONS)


@dataclass(frozen=True)
class Tile:
    symbol: str


STARTING_TILE = Tile('S')
GROUND = Tile('.')


@dataclass(frozen=True)
class Pipe(Tile):
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


class Map:
    def __init__(self, tiles: List[List[Tile]]) -> None:
        self.tiles = tiles

        self._loop: Optional[List[Position]] = None
        self._side_tiles: Dict[Orientation, Set[Position]] = {}

        self.starting_position = self._get_starting_position()
        self._set_loop()

    @classmethod
    def from_text(cls, text: str):
        tiles: List[List[Tile]] = []
        for line in text.splitlines(keepends=False):
            tiles.append([parse_tile(char) for char in line])
        return cls(tiles=tiles)

    @property
    def width(self):
        return len(self.tiles[0])

    @property
    def height(self):
        return len(self.tiles)

    def get_loop(self):
        assert self._loop is not None
        return self._loop

    def get_side_tiles(self):
        return self._side_tiles

    def iter_positions(self) -> Iterator[Position]:
        """
        Yield all positions for the map. Positions closer to the edges are yielded first.
        """
        min_y = 0
        max_y = self.height - 1
        min_x = 0
        max_x = self.width - 1
        while min_y <= max_y and min_x <= max_x:
            for x in range(min_x, max_x + 1):
                yield Position(x, min_y)
                if min_y < max_y:
                    yield Position(x, max_y)

            min_y += 1
            max_y -= 1

            for y in range(min_y, max_y + 1):
                yield Position(min_x, y)
                if min_x < max_x:
                    yield Position(max_x, y)

            min_x += 1
            max_x -= 1

    def _get_starting_position(self):
        for position in self.iter_positions():
            if self.get(position) == STARTING_TILE:
                return position
        raise RuntimeError("Can't find starting position")

    def is_outside(self, position: Position):
        return position.x < 0 or position.y < 0 or position.x >= self.width or position.y >= self.height

    def get(self, position: Position):
        if not self.is_outside(position):
            return self.tiles[position.y][position.x]
        return None

    def get_connected_pipe(self, origin: Position, direction: Direction):
        """
        Look for a tile going from ``origin`` to ``direction``, and if there is a pipe there that’s connected to
        ``origin``, return a tuple of ``(new_position, pipe, next_direction)`` where ``new_position`` is the position of
        the pipe tile and ``next_direction`` is the next direction to use to follow the pipe.
        """
        new_position = origin.go_to(direction)
        pipe = self.get(new_position)
        if not isinstance(pipe, Pipe):
            return None

        direction_to_origin = direction.opposite()

        if pipe.is_connected(direction_to_origin):
            return new_position, pipe, pipe.opposite_end(direction_to_origin)

        return None

    def get_initial_pipe(self) -> tuple[Position, Pipe, Direction]:
        for direction in DIRECTIONS:
            if initial_pipe := self.get_connected_pipe(self.starting_position, direction):
                return initial_pipe
        raise RuntimeError("Can't find initial pipe")

    def _set_loop(self) -> None:
        loop_positions = [self.starting_position]

        side_tiles: Dict[Orientation, Set[Position]] = {
            orientation: set() for orientation in list(Orientation)
        }

        new_position, pipe, next_direction = self.get_initial_pipe()

        while new_position != self.starting_position:
            loop_positions.append(new_position)

            prev_direction = pipe.opposite_end(next_direction).opposite()

            for orientation in Orientation:
                for direction in (prev_direction, next_direction):
                    orientation_direction = direction.get_direction_from_orientation(orientation)
                    orientation_position = new_position.go_to(orientation_direction)
                    if not self.is_outside(orientation_position):
                        side_tiles[orientation].add(orientation_position)

            next_pipe = self.get_connected_pipe(new_position, next_direction)
            if next_pipe is None:
                assert new_position.go_to(next_direction) == self.starting_position
                break

            new_position, pipe, next_direction = next_pipe

        for orientation_tiles in side_tiles.values():
            orientation_tiles.difference_update(loop_positions)

        self._loop = loop_positions
        self._side_tiles = side_tiles

        for side_tiles_set in self._side_tiles.values():
            self._expand_side_tiles(side_tiles_set)

    def _expand_side_tiles(self, tiles: Set[Position]):
        loop_positions = set(self.get_loop())
        while True:
            size = len(tiles)
            for position in list(tiles):
                # Not very efficient
                for neighbor in position.iter_neighbors():
                    if self.is_outside(neighbor):
                        continue

                    if neighbor not in loop_positions:
                        tiles.add(neighbor)

            if len(tiles) == size:
                break

    def get_outside_positions(self) -> Set[Position]:
        """Return all positions that are directly connected to an edge of the map."""
        loop_positions = set(self.get_loop())
        outside_positions: Set[Position] = set()

        for position in self.iter_positions():
            if position in loop_positions:
                continue

            if any(
                    self.is_outside(neighbor) or neighbor in outside_positions
                    for neighbor in position.iter_neighbors()
            ):
                outside_positions.add(position)
                continue

        return outside_positions

    def show(self) -> None:
        loop_positions = set(self.get_loop())

        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                position = Position(x, y)

                colors: List[str] = []

                if position in self._side_tiles[Orientation.PORTSIDE]:
                    colors.extend((Back.RED, Fore.WHITE))
                elif position in self._side_tiles[Orientation.STARBOARD]:
                    colors.extend((Back.GREEN, Fore.WHITE))

                if position not in loop_positions:
                    colors.append(Style.DIM)

                print(c(tile.symbol, *colors) if colors else tile.symbol, end="")
            print()


def problem1(text: str):
    return len(Map.from_text(text).get_loop()) // 2


def problem2(text: str):
    m = Map.from_text(text)

    if all(not s for s in m.get_side_tiles().values()):
        return 0

    outside_positions = m.get_outside_positions()

    side_tiles_sets = list(m.get_side_tiles().values())
    # If one side overlaps outside tiles, return the size of the other
    for i, side_tiles_set in enumerate(side_tiles_sets):
        if side_tiles_set & outside_positions:
            return len(side_tiles_sets[(i + 1) % 2])

    # There are no outside tiles
    return sum(map(len, side_tiles_sets))


if __name__ == '__main__':
    aoc.run(problem1, problem2)
