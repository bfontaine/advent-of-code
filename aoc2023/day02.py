from dataclasses import dataclass
from typing import List

import aoc


@dataclass
class ColorSelection:
    blue: int = 0
    red: int = 0
    green: int = 0

    @classmethod
    def from_string(cls, s: str):
        record = cls()
        for color_record in s.split(", "):
            n, color = color_record.split(" ")
            setattr(record, color, int(n))
        return record

    def subset_of(self, selection: "ColorSelection"):
        return self.blue <= selection.blue \
            and self.red <= selection.red \
            and self.green <= selection.green

    def power(self):
        """
        > The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
        """
        return self.blue * self.red * self.green


@dataclass
class Game:
    n: int
    records: List[ColorSelection]

    @classmethod
    def from_string(cls, line: str):
        game_str, records_str = line.split(": ")
        records = [ColorSelection.from_string(record_str) for record_str in records_str.split("; ")]
        return cls(
            n=int(game_str.replace("Game ", "")),
            records=records,
        )

    def possible_with(self, selection: ColorSelection):
        """
        Test if the game would have been possible with the given selection of colors.
        """
        return all(
            record.subset_of(selection)
            for record in self.records
        )

    def minimal_selection(self):
        """
        Return the minimal selection for which this game would have been possible.
        """
        return ColorSelection(
            blue=max(r.blue for r in self.records),
            red=max(r.red for r in self.records),
            green=max(r.green for r in self.records),
        )


def problem1(text: str):
    selection = ColorSelection(red=12, green=13, blue=14)

    s = 0
    for line in text.splitlines():
        game = Game.from_string(line)
        if game.possible_with(selection):
            s += game.n

    return s


def problem2(text: str):
    s = 0
    for line in text.splitlines():
        game = Game.from_string(line)
        s += game.minimal_selection().power()

    return s


if __name__ == '__main__':
    aoc.run(problem1, problem2)
