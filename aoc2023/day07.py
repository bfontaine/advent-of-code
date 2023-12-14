from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Dict, List, Optional, Tuple

import aoc

JOKER_VALUE = 1
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


def get_card_value(c: str, with_joker=False):
    if with_joker and c == "J":
        return JOKER_VALUE

    return CARD_VALUES[c]


def get_card_for_value(n: int, with_joker=False):
    if with_joker and n == JOKER_VALUE:
        return "J"
    return VALUE_TO_CARD[n]


class HandType(int, Enum):
    high_card = 1
    one_pair = 2
    two_pair = 3
    three_of_a_kind = 4
    full_house = 5
    four_of_a_kind = 6
    five_of_a_kind = 7


def get_hand_distribution(cards: List[int]):
    return [n for _, n in Counter(cards).most_common()]


def _find_hand_type(cards: List[int]):
    counts = get_hand_distribution(cards)

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


def _find_hand_type_with_joker(cards: List[int]):
    if JOKER_VALUE not in cards:
        return _find_hand_type(cards)

    jokers = cards.count(JOKER_VALUE)
    # JJJJJ -> AAAAA
    # J... A -> A... A
    # J... -> A...
    if jokers in {4, 5}:
        return HandType.five_of_a_kind

    counts = get_hand_distribution([c for c in cards if c != JOKER_VALUE])
    # only As -> J=A -> five of a kind
    if len(counts) == 1:
        return HandType.five_of_a_kind

    if jokers == 3:
        # JJJ12 -> 11112
        assert len(counts) == 2
        return HandType.four_of_a_kind

    if jokers == 2:
        # JJ233 -> 33233
        if len(counts) == 2:
            return HandType.four_of_a_kind
        # JJ123 -> 11123
        assert len(counts) == 3
        return HandType.three_of_a_kind

    assert jokers == 1
    match counts:
        case [3, 1]:  # J1112 -> 11112
            return HandType.four_of_a_kind
        case [2, 2]:  # J1122 -> 21122
            return HandType.full_house
        case [2, 1, 1]:  # J1123 -> 11123
            return HandType.three_of_a_kind
        case [1, 1, 1, 1]:  # J1234 -> 11234
            return HandType.one_pair

    assert False, f"Cannot determine type of {cards} with joker (jokers={jokers}, counts={counts})"


@total_ordering
@dataclass
class Hand:
    cards: List[int]
    with_joker: bool = False
    _type: Optional[HandType] = None

    @property
    def type(self):
        if self._type is None:
            if self.with_joker:
                self._type = _find_hand_type_with_joker(self.cards)
            else:
                self._type = _find_hand_type(self.cards)
        return self._type

    @classmethod
    def from_string(cls, s: str, with_joker=False):
        return cls(
            cards=[get_card_value(c, with_joker=with_joker) for c in s],
            with_joker=with_joker,
        )

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
        cards_str = "".join(get_card_for_value(n, with_joker=self.with_joker) for n in self.cards)
        return f"{self.__class__.__name__}({cards_str}, {self.type})"


def parse_hands(text: str, with_joker=False):
    hands_with_bids: List[Tuple[Hand, int]] = []
    for line in text.splitlines(keepends=True):
        cards_str, bid_str = line.split(" ", 1)
        hands_with_bids.append((Hand.from_string(cards_str, with_joker=with_joker), int(bid_str)))

    return hands_with_bids


def get_total_winning(text: str, with_joker=False):
    hands_with_bids = parse_hands(text, with_joker=with_joker)
    hands_with_bids.sort()

    total_winning = sum((i + 1) * bid for i, (_, bid) in enumerate(hands_with_bids))

    return total_winning


def problem1(text: str):
    return get_total_winning(text)


def problem2(text: str):
    # 251333198 = too low
    return get_total_winning(text, with_joker=True)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
