import itertools
from dataclasses import dataclass
from typing import List

import aoc


@dataclass
class Universe:
    rows: List[List[bool]]

    @classmethod
    def from_string(cls, s: str):
        return cls(
            rows=[
                [c == '#' for c in line]
                for line in s.splitlines(keepends=False)
            ]
        )

    @property
    def width(self):
        return len(self.rows[0])

    def _expand_rows(self):
        empty_row = [False] * self.width
        offset = 0
        for i, row in list(enumerate(self.rows)):
            if any(row):
                continue

            self.rows.insert(i + offset, list(empty_row))
            offset += 1

    def _expand_columns(self):
        offset = 0
        for i in range(self.width):
            if any(row[i + offset] for row in self.rows):
                continue

            for row in self.rows:
                row.insert(i + offset, False)
            offset += 1

    def expand(self):
        self._expand_columns()
        self._expand_rows()

    def get_galaxies(self):
        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                if c:
                    yield x, y


def problem1(text: str):
    universe = Universe.from_string(text)
    universe.expand()
    galaxies = universe.get_galaxies()
    pairs = itertools.combinations(galaxies, 2)
    distances = [(abs(x1 - x2) + abs(y1 - y2)) for (x1, y1), (x2, y2) in pairs]
    return sum(distances)


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
