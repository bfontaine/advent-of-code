from dataclasses import dataclass

import aoc


@dataclass
class Race:
    time: int
    record_distance: int

    def possible_wins(self):
        wins = 0
        for n in range(1, self.time):
            if n * (self.time - n) > self.record_distance:
                wins += 1

        return wins


"""
0 <= X <= T

R = record distance

distance = (T - X) * X

distance = (T - 0) * 0
    ->
distance = (T - T) * T

0 * T
1 * (T-1)
2 * (T-3)
...
T * (T-T)
"""


def parse_races(text: str):
    times, record_distances = [
        [int(n) for n in line.split(":", 1)[1].strip().split()]
        for line in text.splitlines(keepends=False)
    ]
    return [Race(time, distance) for time, distance in zip(times, record_distances)]


def problem1(text: str):
    races = parse_races(text)

    wins_score = races[0].possible_wins()
    for race in races[1:]:
        wins_score *= race.possible_wins()

    return wins_score


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
