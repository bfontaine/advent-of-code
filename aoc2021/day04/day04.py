# -*- coding: UTF-8 -*-

import re
import sys
import argparse
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
    p = argparse.ArgumentParser()
    p.add_argument("--p2", action="store_true")
    p2 = p.parse_args().p2
    numbers_string, *board_strings = sys.stdin.read().split("\n\n")
    numbers = (int(n) for n in numbers_string.split(","))
    # collection with ~O(1) deletion
    boards = {i: Board.from_string(s) for i, s in enumerate(board_strings)}

    for number in numbers:
        is_last = len(boards) == 1

        for i, b in tuple(boards.items()):
            if b.play(number):
                if p2:
                    if is_last:
                        print(b.score() * number)
                        return

                    del boards[i]
                else:
                    print(b.score() * number)
                    return


if __name__ == "__main__":
    main()
