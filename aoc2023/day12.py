import itertools
from dataclasses import dataclass
from enum import Enum
from typing import List, Iterable, Tuple

import clj

import aoc


class Condition(str, Enum):
    # It's easier to think with empty/present rather than operational/damaged
    EMPTY = "."  # = operational
    PRESENT = "#"  # = damaged
    UNKNOWN = "?"


@dataclass
class Record:
    conditions: List[Condition]
    groups: List[int]

    @property
    def size(self):
        return len(self.conditions)

    @classmethod
    def from_string(cls, s: str):
        conditions_str, groups_str = s.split(" ", 1)
        return cls(
            conditions=[Condition(c) for c in conditions_str],
            groups=[int(n) for n in groups_str.split(",")],
        )

    def __str__(self):
        conditions_str = "".join(self.conditions)
        groups_str = ",".join(str(n) for n in self.groups)
        return f"{conditions_str} {groups_str}"

    def get_condition(self, idx: int):
        if idx < 0 or idx >= self.size:
            return None
        return self.conditions[idx]

    def get_raw_possible_group_positions(self) -> List[range]:
        group_position_ranges: List[range] = []
        min_x = 0

        for i, group in enumerate(self.groups):
            # Special case when the first position is 'present'
            if i == 0 and self.conditions[0] == Condition.PRESENT:
                group_position_ranges.append(range(0, 1))
                min_x += group + 1
                continue

            right_groups = self.groups[i + 1:]
            right_margin = sum(right_groups) + len(right_groups)
            max_x = self.size - right_margin - group

            # in the examples below, group=3

            # [???.] -> [???].
            while self.get_condition(min_x) == Condition.EMPTY:
                min_x += 1

            # [.???] -> .[???]
            while self.get_condition(max_x + group - 1) == Condition.EMPTY:
                max_x -= 1

            group_position_ranges.append(range(min_x, max_x + 1))
            min_x += group + 1

        return group_position_ranges

    def _filter_possible_group_positions(self, r: range, group: int):
        valid_xs: List[int] = []
        for x in r:
            if Condition.EMPTY in self.conditions[x:x + group]:
                continue

            valid_xs.append(x)

        return valid_xs

    def get_possible_group_positions(self) -> List[List[int]]:
        group_positions: List[List[int]] = []
        for i, r in enumerate(self.get_raw_possible_group_positions()):
            conditions = self._filter_possible_group_positions(r, self.groups[i])
            group_positions.append(conditions)

        return group_positions

    def _is_arrangement_possible(self, arrangement: Tuple[int, ...]):
        arrangement = tuple(arrangement + tuple([self.size + 1]))

        for i, x in enumerate(arrangement):
            if i == len(arrangement) - 1:
                break

            # no 'present' between the beginning of the record and the first group
            if i == 0 and Condition.PRESENT in self.conditions[:x]:
                return False

            # No 'present' before the group
            if self.get_condition(x - 1) == Condition.PRESENT:
                return False

            x_after_group = x + self.groups[i]

            # no overlap between groups
            if x_after_group + 1 > arrangement[i + 1]:
                return False

            # no 'present' between groups
            if Condition.PRESENT in self.conditions[x_after_group: arrangement[i + 1]]:
                return False

        return True

    def get_possible_arrangements(self) -> Iterable[Tuple[int, ...]]:
        for arrangement in itertools.product(*self.get_possible_group_positions()):
            if self._is_arrangement_possible(arrangement):
                yield arrangement

    def count_possible_arrangements(self):
        return clj.count(self.get_possible_arrangements())


def parse_records(text: str):
    return [
        Record.from_string(line)
        for line in text.splitlines(keepends=False)
    ]


def problem1(text: str):
    records = parse_records(text)

    total = 0
    for record in records:
        total += record.count_possible_arrangements()

    return total


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
