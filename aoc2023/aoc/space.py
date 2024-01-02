import enum
from typing import NamedTuple


class Orientation(int, enum.Enum):
    # https://en.wikipedia.org/wiki/Port_and_starboard
    PORTSIDE = enum.auto()  # "left"
    STARBOARD = enum.auto()  # "right"


class Direction(NamedTuple):
    dx: int
    dy: int

    def opposite(self):
        return Direction(-self.dx, -self.dy)

    def turn(self, orientation: Orientation) -> "Direction":
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

    def apply(self, x: int, y: int, *, force=1):
        return x + self.dx * force, y + self.dy * force

    def __repr__(self):
        return f"{self.__class__.__name__}<{DIRECTION_SYMBOLS[DIRECTIONS.index(self)]}>"

    @classmethod
    def from_char(cls, c: str) -> "Direction":
        if c in DIRECTION_SYMBOLS:
            return DIRECTIONS[DIRECTION_SYMBOLS.index(c)]

        # up/right/down/left (day 18, 2023)
        if c in ALT_DIRECTION_SYMBOLS:
            return DIRECTIONS[ALT_DIRECTION_SYMBOLS.index(c)]

        raise ValueError(f"Unrecognized direction: {c}")


NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
DIRECTION_SYMBOLS = "NESW"
ALT_DIRECTION_SYMBOLS = "URDL"  # up/right/down/left (day 18, 2023)


class Position(NamedTuple):
    x: int
    y: int

    def go_to(self, direction: Direction, force=1):
        x1, y1 = direction.apply(self.x, self.y, force=force)
        return Position(x=x1, y=y1)

    def iter_neighbors(self):
        return (self.go_to(direction) for direction in DIRECTIONS)
