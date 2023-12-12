from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, List, Dict

import aoc

XY = Tuple[int, int]


@dataclass
class Item:
    x: int
    y: int


@dataclass
class Number(Item):
    value: int


@dataclass
class Symbol(Item):
    value: str


@dataclass
class Grid:
    text: str
    height: int
    width: int

    @classmethod
    def from_string(cls, s: str):
        return cls(
            height=s.rstrip("\n").count("\n") + 1,
            width=s.index("\n"),
            text=s.replace("\n", ""),
        )

    def __getitem__(self, xy: XY):
        x, y = xy
        i = y * self.width + x
        return self.text[i]

    def get_numbers_and_symbols(self) -> Tuple[List[Number], List[Symbol]]:
        """
        Collect numbers and symbols in the grid.
        """
        numbers: List[Number] = []
        symbols: List[Symbol] = []

        for y in range(0, self.height):
            x = 0
            while x < self.width:
                c = self[x, y]
                if c == ".":
                    x += 1
                elif c.isnumeric():
                    number_x = x
                    number_chars = []
                    while c.isnumeric():
                        number_chars.append(c)
                        x += 1
                        c = self[x, y]

                    numbers.append(Number(x=number_x, y=y, value=int("".join(number_chars))))
                else:
                    symbols.append(Symbol(x=x, y=y, value=c))
                    x += 1

        return numbers, symbols


def problem1(text: str):
    grid = Grid.from_string(text)

    numbers, symbols = grid.get_numbers_and_symbols()

    symbols_coordinates = set((s.x, s.y) for s in symbols)

    s = 0
    for number in numbers:
        x1 = number.x
        x2 = number.x + len(str(number.value))
        y = number.y

        for y1 in (y - 1, y, y + 1):
            for x in range(x1 - 1, x2 + 1):
                if (x, y1) in symbols_coordinates:
                    s += number.value

    return s


def problem2(text: str):
    grid = Grid.from_string(text)

    numbers, symbols = grid.get_numbers_and_symbols()

    potential_gear_coordinates = set(
        (s.x, s.y)
        for s in symbols
        if s.value == "*"
    )

    # (gear_x, gear_y) -> [n, n, ...]
    gears_numbers: Dict[XY, List[int]] = defaultdict(list)

    s = 0
    for number in numbers:
        x1 = number.x
        x2 = number.x + len(str(number.value))
        y = number.y

        for y1 in (y - 1, y, y + 1):
            for x in range(x1 - 1, x2 + 1):
                if (x, y1) in potential_gear_coordinates:
                    gears_numbers[x, y1].append(number.value)

    for gear_numbers in gears_numbers.values():
        if len(gear_numbers) != 2:
            continue

        gear_ratio = gear_numbers[0] * gear_numbers[1]
        s += gear_ratio

    return s


if __name__ == '__main__':
    aoc.run(problem1, problem2)
