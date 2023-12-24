from typing import List

import aoc
from aoc.containers import Grid


def _is_reflection_line(line: int, lookup: List[str], max_line: int, smudge=False):
    before = "".join([lookup[x] for x in range(line - 1, -1, -1)])
    after = "".join([lookup[x] for x in range(line, max_line)])

    if not smudge:
        size = min(len(before), len(after))
        return before[:size] == after[:size]

    smudged = False
    for a, b in zip(before, after):
        if a != b:
            if smudged:
                return False
            smudged = True

    return smudged


class Pattern(Grid):
    def is_vertical_reflection_line(self, line_x: int, smudge=False):
        return _is_reflection_line(line_x, self.columns, self.width, smudge=smudge)

    def is_horizontal_reflection_line(self, line_y: int, smudge=False):
        return _is_reflection_line(line_y, self.rows, self.height, smudge=smudge)

    def find_vertical_line(self, smudge=False):
        for line_x in range(1, self.width):
            if self.is_vertical_reflection_line(line_x, smudge=smudge):
                return line_x
        return 0

    def find_horizontal_line(self, smudge=False):
        for line_y in range(1, self.height):
            if self.is_horizontal_reflection_line(line_y, smudge=smudge):
                return line_y
        return 0

    def reflection_score(self, smudge=False):
        if v := self.find_vertical_line(smudge=smudge):
            return v

        return 100 * self.find_horizontal_line(smudge=smudge)


def parse_patterns(text: str):
    pattern_rows: List[str] = []

    for line in text.splitlines():
        if not line:
            yield Pattern(pattern_rows)
            pattern_rows = []
            continue

        pattern_rows.append(line)

    yield Pattern(pattern_rows)


def problem1(text: str):
    total = 0
    for pattern in parse_patterns(text):
        total += pattern.reflection_score()

    return total


def problem2(text: str):
    total = 0
    for pattern in parse_patterns(text):
        total += pattern.reflection_score(smudge=True)

    return total


if __name__ == '__main__':
    aoc.run(problem1, problem2)
