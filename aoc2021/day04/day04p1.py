# -*- coding: UTF-8 -*-

import re
import sys
from typing import List, Set

SIZE = 5

class Board:
    def __init__(self):
        # lines then columns
        self._rows: List[Set] = [set() for _ in range(SIZE*2)]

    @classmethod
    def from_string(cls, s: str):
        lines: List[List[int]] = []

        for line_string in s.rstrip().splitlines():
            lines.append([int(n) for n in re.split(r" +", line_string.strip())])

        b = cls()

        for y in range(SIZE):
            for x in range(SIZE):
                el = lines[y][x]
                b._rows[y].add(el)
                b._rows[SIZE + x].add(el)

        return b

    def play(self, n: int):
        won = False

        for row in self._rows:
            if n in row:
                row.remove(n)
                if not row:
                    won = True

        return won

    def score(self):
        return sum(set.union(*self._rows))



def main():
    numbers_string, *board_strings = sys.stdin.read().split("\n\n")
    numbers = (int(n) for n in numbers_string.split(","))
    boards = [Board.from_string(s) for s in board_strings]

    for number in numbers:
        for b in boards:
            if b.play(number):
                print(b.score() * number)
                return


if __name__ == "__main__":
    main()
