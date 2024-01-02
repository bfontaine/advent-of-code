import itertools
from typing import List, Set

import aoc
from aoc.space import Position


class Universe:
    def __init__(self, rows: List[List[bool]]):
        self.rows = rows
        self._set_expanded_rows()
        self._set_expanded_columns()

    @classmethod
    def from_string(cls, s: str):
        return cls(
            rows=[
                [c == '#' for c in line]
                for line in s.splitlines()
            ]
        )

    @property
    def width(self):
        return len(self.rows[0])

    def _set_expanded_rows(self):
        self._expanded_rows: Set[int] = set()
        for y, row in list(enumerate(self.rows)):
            if not any(row):
                self._expanded_rows.add(y)

    def _set_expanded_columns(self):
        self._expanded_columns: Set[int] = set()
        for x in range(self.width):
            if not any(row[x] for row in self.rows):
                self._expanded_columns.add(x)

    def get_galaxies(self):
        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                if c:
                    yield Position(x, y)

    def distance(self, p1: Position, p2: Position, expansion_factor=1):
        x1, x2 = sorted((p1.x, p2.x))
        y1, y2 = sorted((p1.y, p2.y))

        expanded_columns = len(self._expanded_columns.intersection(range(x1 + 1, x2)))
        expanded_rows = len(self._expanded_rows.intersection(range(y1 + 1, y2)))

        horizontal_distance = x2 - x1 + expanded_columns * (expansion_factor - 1)
        vertical_distance = y2 - y1 + expanded_rows * (expansion_factor - 1)

        return horizontal_distance + vertical_distance


def get_sum_of_galaxies_distances(text: str, *, expansion_factor=1):
    universe = Universe.from_string(text)
    galaxies = universe.get_galaxies()
    pairs = itertools.combinations(galaxies, 2)
    distances = [universe.distance(p1, p2, expansion_factor=expansion_factor) for p1, p2 in pairs]
    return sum(distances)


def problem1(text: str):
    return get_sum_of_galaxies_distances(text, expansion_factor=2)


def problem2(text: str):
    return get_sum_of_galaxies_distances(text, expansion_factor=1000000)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
