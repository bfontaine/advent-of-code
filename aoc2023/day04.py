from collections import Counter
from typing import Dict, Counter as CounterType

import aoc


def parse_card_matches(line: str):
    card_content = line.split(":", 1)[1]
    numbers_parts = card_content.split("|", 1)
    winning_numbers, card_numbers = [
        set(map(int, numbers.strip().split()))
        for numbers in numbers_parts
    ]
    return len(winning_numbers & card_numbers)


def problem1(text: str):
    s = 0
    for line in text.splitlines():
        matches = parse_card_matches(line)
        if matches:
            s += 2 ** (matches - 1)

    return s


def problem2(text: str):
    # how many matches does each card have?
    card_matches: Dict[int, int] = {}

    # how many times do we have each card?
    cards: CounterType[int] = Counter()

    for i, line in enumerate(text.splitlines()):
        card_matches[i + 1] = parse_card_matches(line)
        cards[i + 1] = 1

    # process each card in increasing order
    for card_number in sorted(cards):
        n = card_matches[card_number]
        for i in range(card_number + 1, card_number + 1 + n):
            cards[i] += cards[card_number]

    return sum(cards.values())


if __name__ == '__main__':
    aoc.run(problem1, problem2)
