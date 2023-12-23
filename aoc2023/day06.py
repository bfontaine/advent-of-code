from dataclasses import dataclass

import aoc


@dataclass
class Race:
    time: int
    record_distance: int

    def possible_wins(self):
        n = 0
        for n in range(self.time + 1):
            if n * (self.time - n) > self.record_distance:
                break

        return (self.time - n) - n + 1


def parse_ints(line: str, ignore_spaces=False):
    line = line.split(":", 1)[1].strip()
    if ignore_spaces:
        line = line.replace(" ", "")

    return [int(n) for n in line.split()]


def parse_races(text: str, ignore_spaces=False):
    times, record_distances = [
        parse_ints(line, ignore_spaces=ignore_spaces)
        for line in text.splitlines()
    ]
    return [Race(time, distance) for time, distance in zip(times, record_distances)]


def get_wins_score(text: str, ignore_spaces=False):
    races = parse_races(text, ignore_spaces)

    wins_score = races[0].possible_wins()
    for race in races[1:]:
        wins_score *= race.possible_wins()

    return wins_score


def problem1(text: str):
    return get_wins_score(text)


def problem2(text: str):
    return get_wins_score(text, ignore_spaces=True)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
