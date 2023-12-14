from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Dict, List, Optional, Tuple

import aoc

CARD_VALUES: Dict[str, int] = {
    **{
        card: 10 + i
        for i, card in enumerate("TJQKA")
    },
    **{
        str(i): i
        for i in range(2, 9 + 1)
    }
}
VALUE_TO_CARD: Dict[int, str] = {value: card for card, value in CARD_VALUES.items()}


class HandType(int, Enum):
    high_card = 1
    one_pair = 2
    two_pair = 3
    three_of_a_kind = 4
    full_house = 5
    four_of_a_kind = 6
    five_of_a_kind = 7


def _find_hand_type(cards: List[int]):
    counts = [n for _, n in Counter(cards).most_common()]

    match counts:
        case [5]:
            return HandType.five_of_a_kind

        case [4, 1]:
            return HandType.four_of_a_kind

        case [3, 2]:
            return HandType.full_house

        case [3, 1, 1]:
            return HandType.three_of_a_kind

        case [2, 2, 1]:
            return HandType.two_pair

        case [2, 1, 1, 1]:
            return HandType.one_pair

        case [1, 1, 1, 1, 1]:
            return HandType.high_card

        case _:
            raise ValueError(f"Can't get hand type from {cards}")


@total_ordering
@dataclass
class Hand:
    cards: List[int]
    _type: Optional[HandType] = None

    @property
    def type(self):
        if self._type is None:
            self._type = _find_hand_type(self.cards)
        return self._type

    @classmethod
    def from_string(cls, s: str):
        return cls(cards=[CARD_VALUES[c] for c in s])

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise ValueError(f"{self} cannot be compared to {other}")

        my_type = self.type
        other_type = other.type

        if my_type < other_type:
            return True

        if my_type > other_type:
            return False

        for my_card, other_card in zip(self.cards, other.cards):
            if my_card < other_card:
                return True
            if my_card > other_card:
                return False

        return False

    def __repr__(self):
        cards_str = "".join(VALUE_TO_CARD[c] for c in self.cards)
        return f"{self.__class__.__name__}({cards_str}, {self.type})"


def parse_hands(text: str):
    hands_with_bids: List[Tuple[Hand, int]] = []
    for line in text.splitlines(keepends=True):
        cards_str, bid_str = line.split(" ", 1)
        hands_with_bids.append((Hand.from_string(cards_str), int(bid_str)))

    return hands_with_bids


def problem1(text: str):
    hands_with_bids = parse_hands(text)
    hands_with_bids.sort()

    total_winning = sum((i + 1) * bid for i, (_, bid) in enumerate(hands_with_bids))

    return total_winning


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
