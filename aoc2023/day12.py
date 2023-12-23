from dataclasses import dataclass
from typing import List

import aoc

# It's easier to think with empty/present rather than operational/damaged
EMPTY = "."  # = operational
PRESENT = "#"  # = damaged
UNKNOWN = "?"


@dataclass
class Record:
    conditions: str
    groups: List[int]
    _str: str

    @property
    def size(self):
        return len(self.conditions)

    @classmethod
    def from_string(cls, s: str, folds=1):
        conditions_str, groups_str = s.split(" ", 1)

        conditions_str = "?".join([conditions_str] * folds)
        groups_str = ",".join([groups_str] * folds)

        return cls(
            conditions=conditions_str,
            groups=[int(n) for n in groups_str.split(",")],
            _str=s,
        )

    def __str__(self):
        return self._str

    def count_possible_arrangements(self) -> int:
        return 42  # TODO


def count_all_possible_arrangements(text: str, folds=1):
    total = 0
    for line in text.splitlines(keepends=False):
        record = Record.from_string(line, folds=folds)
        total += record.count_possible_arrangements()

    return total


def problem1(text: str):
    return count_all_possible_arrangements(text)


def problem2(text: str):
    return count_all_possible_arrangements(text, folds=5)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
