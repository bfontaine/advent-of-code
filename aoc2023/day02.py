from typing import List

from pydantic import BaseModel

import aoc


class ColorSelection(BaseModel):
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


class Game(BaseModel):
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
        return all(
            record.subset_of(selection)
            for record in self.records
        )


def problem1(text: str):
    selection = ColorSelection(red=12, green=13, blue=14)

    s = 0
    for line in text.splitlines():
        game = Game.from_string(line)
        if game.possible_with(selection):
            s += game.n

    return s


if __name__ == '__main__':
    aoc.run(problem1)
