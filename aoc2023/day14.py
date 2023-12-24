import re

import aoc
from aoc.containers import Grid

ROUNDED_ROCK = "O"
CUBE_ROCK = "#"
EMPTY = "."


class Support(Grid):
    pass


def _reorder_rolled_rocks(m: re.Match):
    positions = m.group(0)
    # reverse so that "O" < "."
    return "".join(sorted(positions, reverse=True))


def roll_column(column: str):
    return re.sub(r"[O.]+", _reorder_rolled_rocks, column)


def problem1(text: str):
    support = Support.from_string(text)

    total_load = 0
    for column in support.columns:
        rolled_column = roll_column(column)

        for i, c in enumerate(rolled_column):
            if c == ROUNDED_ROCK:
                load = support.height - i
                total_load += load

    return total_load


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
