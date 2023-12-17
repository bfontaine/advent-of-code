import day07
from day07 import Hand
from aoc import assert_examples, get_input_data


def test_card_values():
    assert day07.CARD_VALUES["T"] == 10
    assert day07.CARD_VALUES["9"] == 9
    assert day07.CARD_VALUES["A"] == 14


def test_get_hand_distribution():
    assert day07.get_hand_distribution([8, 10, 9, 10]) == [2, 1, 1]


def test_compare_hands():
    h1 = Hand.from_string("KTJJT")
    h2 = Hand.from_string("KK677")
    assert h1 < h2


def test_compare_hands_with_joker():
    h1 = Hand.from_string("KTJJT", with_joker=True)
    h2 = Hand.from_string("KK677", with_joker=True)
    assert h1 > h2


def test_problem1_examples():
    assert_examples(day07.problem1)


def test_problem2_examples():
    assert_examples(day07.problem2)
