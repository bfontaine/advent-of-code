from dataclasses import dataclass
from typing import List, Iterable

import aoc

# It's easier to think with empty/present rather than operational/damaged
EMPTY = "."  # = operational
PRESENT = "#"  # = damaged
UNKNOWN = "?"


def _product(all_positions: List[List[int]], groups: List[int]) -> Iterable[List[int]]:
    partial_groups_positions: Iterable[List[int]] = [[]]

    for i, group_positions in enumerate(all_positions):
        partial_groups_positions = [
            partial_group_positions + [position]
            for partial_group_positions in partial_groups_positions
            for position in group_positions
            if i == 0 or (
                    partial_group_positions[-1] + groups[i - 1] < position
            )
        ]
    return partial_groups_positions


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

    def get_raw_possible_group_positions(self) -> List[List[int]]:
        """
        Return a list of ranges representing the possible starting positions of each group.
        This needs to be filtered down because it includes impossible arrangements.
        """
        group_position_ranges: List[List[int]] = []
        min_x = 0

        starts_with_present = self.conditions[0] == PRESENT
        ends_with_present = self.conditions[-1] == PRESENT

        for i, group in enumerate(self.groups):
            # Special case when the first position is 'present'
            if starts_with_present and i == 0:
                group_position_ranges.append([0])
                min_x += group + 1
                continue

            # idem for the last one
            if ends_with_present and i == len(self.groups) - 1:
                group_position_ranges.append([self.size - group])
                continue

            right_groups = self.groups[i + 1:]

            right_margin = sum(right_groups) + len(right_groups)
            max_x = self.size - right_margin - group

            # in the examples below, group=3

            # [.???] -> .[???]
            # [??.???] -> ??.[???]
            while EMPTY in self.conditions[min_x:min_x + group]:
                min_x += 1

            # [???.] -> [???].
            # [???.?] -> [???].?
            while EMPTY in self.conditions[max_x:max_x + group]:
                max_x -= 1

            r = [
                x
                for x in range(min_x, max_x + 1)
                if EMPTY not in self.conditions[x:x + group]
            ]

            group_position_ranges.append(r)
            min_x += group + 1

        return group_position_ranges

    def _filter_possible_group_positions(self, r: Iterable[int], group: int):
        """
        Given a range of x's and a group index, return the valid x's the group can start at.
        """
        valid_xs: List[int] = []
        for x in r:
            if EMPTY in self.conditions[x:x + group]:
                continue

            valid_xs.append(x)

        return valid_xs

    def _reduce_possible_group_positions(self, group_positions: List[List[int]]):
        changed = True
        while changed:
            changed = False
            # reduce the possibilities:
            for i in range(len(self.groups)):
                if i > 0:
                    # min_x of a group must be >= min_x of the group before + length of that group + 1
                    prev_group = self.groups[i - 1]
                    if prev_group_positions := group_positions[i - 1]:
                        prev_min_x = prev_group_positions[0]
                        new_positions = [p for p in group_positions[i] if p > prev_min_x + prev_group]
                        if group_positions[i] != new_positions:
                            changed = True
                            group_positions[i] = new_positions

                if i < len(self.groups) - 1:
                    # max_x of a group must be <= max_x of the group after - length of the current group - 1
                    group = self.groups[i]
                    if next_group_positions := group_positions[i + 1]:
                        next_max_x = next_group_positions[-1]
                        new_positions = [p for p in group_positions[i] if p < next_max_x - group]
                        if group_positions[i] != new_positions:
                            changed = True
                            group_positions[i] = new_positions

    def get_possible_group_positions(self) -> List[List[int]]:
        """
        Return a list where [i] contains the possible x's the group[i] can start at.
        """
        group_positions: List[List[int]] = []
        for i, r in enumerate(self.get_raw_possible_group_positions()):
            conditions = self._filter_possible_group_positions(r, self.groups[i])
            group_positions.append(conditions)

        assert len(group_positions) == len(self.groups)

        self._reduce_possible_group_positions(group_positions)

        return group_positions

    def _is_arrangement_possible(self, arrangement: List[int]):
        arrangement = arrangement + [self.size + 1]

        for i, x in enumerate(arrangement):
            if i == len(arrangement) - 1:
                break

            # no 'present' between the beginning of the record and the first group
            if i == 0 and PRESENT in self.conditions[:x]:
                return False

            # No 'present' before the group
            if x > 0 and self.conditions[x - 1] == PRESENT:
                return False

            x_after_group = x + self.groups[i]

            # no overlap between groups
            if x_after_group + 1 > arrangement[i + 1]:
                return False

            # no 'present' between groups
            if PRESENT in self.conditions[x_after_group: arrangement[i + 1]]:
                return False

        return True

    def count_possible_arrangements(self) -> int:
        possible_group_positions = self.get_possible_group_positions()
        total = 0

        # print(possible_group_positions)
        for arrangement in _product(possible_group_positions, self.groups):
            if self._is_arrangement_possible(arrangement):
                total += 1

        return total


def problem1(text: str):
    total = 0
    for line in text.splitlines(keepends=False):
        record = Record.from_string(line)
        total += record.count_possible_arrangements()

    return total


def problem2(text: str):
    total = 0

    for line in text.splitlines(keepends=False):
        print(line)
        f5 = Record.from_string(line, folds=5).count_possible_arrangements()  # XXX not fast enough

        total += f5

    return total


if __name__ == '__main__':
    aoc.run(problem1, problem2)
