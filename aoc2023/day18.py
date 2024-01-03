from typing import Tuple, Iterator

import aoc
from aoc.space import Position, Direction


def parse_dig_plan(text: str, mode: int) -> Iterator[Tuple[Direction, int]]:
    assert mode in {1, 2}

    for line in text.splitlines():
        if mode == 1:
            direction_str, amount_str, _ = line.split()
            amount = int(amount_str)
        else:
            color_code = line.rstrip(")").split("#", 1)[1]
            # > The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.
            direction_str = "RDLU"[int(color_code[-1])]
            amount = int(color_code[:-1], 16)

        yield (
            Direction.from_char(direction_str),
            amount,
        )


def run(text: str, mode: int):
    position = Position(0, 0)
    x2 = y2 = 0

    # https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula
    double_area = 0
    perimeter = 0

    for direction, amount in parse_dig_plan(text, mode=mode):
        x1 = x2
        y1 = y2

        perimeter += amount
        position = position.go_to(direction, amount)
        x2 = position.x
        y2 = position.y

        double_area += (y1 + y2) * (x1 - x2)

    return int(abs(double_area / 2)) + (perimeter + 1) // 2 + 1


def problem1(text: str):
    return run(text, mode=1)


def problem2(text: str):
    return run(text, mode=2)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
