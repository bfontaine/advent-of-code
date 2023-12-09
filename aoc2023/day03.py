from typing import Tuple, List

from pydantic import BaseModel

import aoc


class Item(BaseModel):
    x: int
    y: int


class Number(Item):
    value: int


class Symbol(Item):
    value: str


class Grid(BaseModel):
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

    def __getitem__(self, xy: Tuple[int, int]):
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
    s = 0
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


if __name__ == '__main__':
    aoc.run(problem1)
