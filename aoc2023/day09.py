from typing import List

import aoc

History = List[int]


def parse_histories(text: str):
    histories: List[History] = []
    for line in text.splitlines(keepends=False):
        histories.append([int(n) for n in line.split()])
    return histories


def differences(history: History) -> History:
    return [
        history[i + 1] - history[i]
        for i in range(len(history) - 1)
    ]


def only_zeroes(history: History):
    return all(n == 0 for n in history)


def differences_sequences(history: History) -> List[History]:
    seqs = [history]
    while not only_zeroes(seqs[-1]):
        seqs.append(differences(seqs[-1]))
    return seqs


def extrapolate(history: History) -> int:
    seqs = differences_sequences(history)

    return sum(seq[-1] for seq in seqs)


def problem1(text: str):
    histories = parse_histories(text)

    extrapolated_total = 0

    for history in histories:
        extrapolated_total += extrapolate(history)

    return extrapolated_total


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
