from day08 import problem1, problem2
from aoc import assert_examples


def test_problem1_examples():
    assert_examples(problem1, examples=(0,))


def test_problem2_examples():
    assert problem2("""
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".strip()) == 6
