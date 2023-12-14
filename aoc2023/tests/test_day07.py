import day07
from day07 import Hand
from aoc import assert_examples


def test_card_values():
    assert day07.CARD_VALUES["T"] == 10
    assert day07.CARD_VALUES["9"] == 9
    assert day07.CARD_VALUES["A"] == 14


def test_compare_hands():
    assert Hand.from_string("KTJJT") < Hand.from_string("KK677")


def test_problem1_examples():
    assert_examples(day07.problem1)

# def test_problem2_examples():
#     assert_examples(day07.problem2)
