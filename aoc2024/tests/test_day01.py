from aoc import assert_examples, example_input_data
from day01 import problem1, problem2


def test_problem1_examples():
    assert_examples(problem1)


def test_problem2_examples():
    # Circumvent a parsing issue
    # https://github.com/wimglenn/aocd-example-parser/issues/7
    input_data = example_input_data()
    assert problem2(input_data) == 31
