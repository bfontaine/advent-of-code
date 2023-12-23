from typing import List

import aoc


class Pattern:
    def __init__(self, rows: List[str]):
        self.rows = rows

        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.columns = [
            "".join([row[x] for row in self.rows])
            for x in range(self.width)
        ]

    def get(self, x: int, y: int):
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return None
        return self.rows[y][x]

    def is_vertical_reflection_line(self, lx: int):
        for x in range(self.width - 1):
            x_left = lx - x - 1
            x_right = lx + x
            if x_left < 0 or x_right >= self.width:
                return True

            if self.columns[x_left] != self.columns[x_right]:
                return False

        return True

    def is_horizontal_reflection_line(self, ly: int):
        for y in range(self.height - 1):
            y_up = ly - y - 1
            y_down = ly + y
            if y_up < 0 or y_down >= self.height:
                return True

            if self.rows[y_up] != self.rows[y_down]:
                return False

        return True

    def find_vertical_line(self):
        for lx in range(1, self.width):
            if self.is_vertical_reflection_line(lx):
                return lx
        return 0

    def find_horizontal_line(self):
        for ly in range(1, self.height):
            if self.is_horizontal_reflection_line(ly):
                return ly
        return 0

    def reflection_score(self):
        v = self.find_vertical_line()
        h = self.find_horizontal_line()

        return v + 100 * h


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
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
