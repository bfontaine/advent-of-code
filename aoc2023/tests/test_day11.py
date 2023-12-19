import pytest

from day11 import problem1, problem2, get_sum_of_galaxies_distances
from aoc import assert_examples, get_puzzle


def test_problem1_examples():
    assert_examples(problem1)


def test_problem2_get_sum_of_galaxies_distances_example():
    puzzle = get_puzzle()
    example = puzzle.examples[0]
    expected_response = example.answers[1]
    actual = str(get_sum_of_galaxies_distances(example.input_data, expansion_factor=100))
    assert actual == expected_response
