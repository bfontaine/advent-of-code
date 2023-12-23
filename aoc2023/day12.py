from dataclasses import dataclass
from typing import List, Tuple, Dict

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
        cache: Dict[Tuple[int, int], int] = {}
        # add this to simplify tests on [x+1]
        conditions = self.conditions + EMPTY

        def count(x: int, group_index: int) -> int:
            k = (x, group_index)
            if k not in cache:
                cache[k] = _count(x, group_index)
            return cache[k]

        def _count(x: int, group_index: int) -> int:
            # we 'consumed' all groups
            if group_index >= len(self.groups):
                # ...but there is still a '#' on the right => no solution
                if PRESENT in conditions[x:]:
                    return 0
                # ok
                return 1

            # end of conditions but we haven't 'consumed' all groups => no solution
            if x >= self.size:
                return 0

            # otherwise, general case:
            total = 0

            condition = conditions[x]
            group = self.groups[group_index]

            if condition == EMPTY or condition == UNKNOWN:  # this position *can* be empty
                # number of arrangements where we skip x and don't put a group here
                total += count(x + 1, group_index)

            if (
                    (condition == PRESENT or condition == UNKNOWN)  # this position *can* be present
                    # the group can fit
                    and group <= self.size - x
                    # there are no empty positions in the group space
                    and EMPTY not in conditions[x:x + group]
                    # there is at least one position after the group and it's not '#'
                    # (this test is simpler thanks to the '+ EMPTY' at the beginning)
                    and conditions[x + group] != PRESENT
            ):
                # number of arrangements where we put the group here
                total += count(x + group + 1, group_index + 1)

            return total

        return count(0, 0)


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
