import enum
from dataclasses import dataclass


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

    def apply(self, x: int, y: int):
        return x + self.dx, y + self.dy

    def __repr__(self):
        return f"{self.__class__.__name__}<{DIRECTION_SYMBOLS[DIRECTIONS.index(self)]}"


NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
DIRECTION_SYMBOLS = "NESW"
