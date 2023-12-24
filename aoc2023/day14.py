import re
from typing import List, Tuple, Iterator, Dict

import aoc
from aoc.containers import Grid

ROUNDED_ROCK = "O"
CUBE_ROCK = "#"
EMPTY = "."


def _roll_line(line: str, left=True):
    return re.sub(r"[O.]+",
                  # reverse so that "O" < "."
                  lambda m: "".join(sorted(m.group(0), reverse=left)),
                  line)


def _roll_lines(lines: List[str], left=True):
    return [
        _roll_line(line, left=left)
        for line in lines
    ]


class Support(Grid):
    def _roll_columns(self, north=True):
        self.columns = _roll_lines(self.columns, left=north)
        return self

    def _roll_rows(self, west=True):
        self.rows = _roll_lines(self.rows, left=west)
        return self

    def roll_north(self):
        return self._roll_columns(north=True)

    def roll_south(self):
        return self._roll_columns(north=False)

    def roll_west(self):
        return self._roll_rows(west=True)

    def roll_east(self):
        return self._roll_rows(west=False)

    def cycle(self):
        return (
            self
            .roll_north()
            .roll_west()
            .roll_south()
            .roll_east()
        )

    def iter_rounded_rocks(self) -> Iterator[Tuple[int, int]]:
        return self.iter_chars(ROUNDED_ROCK)

    def north_load(self):
        return sum([
            self.height - y
            for _, y in self.iter_rounded_rocks()
        ])


def problem1(text: str):
    return Support.from_string(text).roll_north().north_load()


def problem2(text: str):
    def support_key(s: Support):
        return "".join(s.rows)

    total_cycles = 1000000000
    i = 0
    k = ""
    seen_support_keys: Dict[str, int] = {}

    support = Support.from_string(text)
    for i in range(total_cycles):
        k = support_key(support)
        if k not in seen_support_keys:
            seen_support_keys[k] = i
        else:
            break

        support.cycle()

    assert i > 0
    assert k

    loop_start_idx = seen_support_keys[k]
    loop_size = i - loop_start_idx
    remaining = (total_cycles - loop_start_idx) % loop_size

    for i in range(remaining):
        support.cycle()

    return support.north_load()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
