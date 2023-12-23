import pytest

from aoc import assert_examples, get_input_data
from day12 import problem1, problem2, Record


@pytest.mark.parametrize("record_str,expected", [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 4),
    ("?###???????? 3,2,1", 10),
    ("?" * 10 + ". 1", 10),
    ("??..????#. 2,2", 2),
])
def test_count_possible_arrangements(record_str, expected):
    r = Record.from_string(record_str)
    assert r.count_possible_arrangements() == expected


@pytest.mark.parametrize("record_str", [
    "? 1",
    "# 1",
    "## 2",
    "### 3",
    "#. 1",
    ".# 1",
    "???.### 1,1,3",
])
def test_count_possible_arrangements_folds2_unchanged(record_str):
    assert Record.from_string(record_str, folds=1).count_possible_arrangements() == 1
    assert Record.from_string(record_str, folds=2).count_possible_arrangements() == 1


@pytest.mark.parametrize("record_str,expected1,expected2", [
    ("??? 1", 3, 15),
    ("????.??#?.?.????# 3,4,1,1", 8, 122),
])
def test_count_possible_arrangements_folds2(record_str, expected1, expected2):
    assert Record.from_string(record_str, folds=1).count_possible_arrangements() == expected1
    assert Record.from_string(record_str, folds=2).count_possible_arrangements() == expected2


def test_problem1_examples():
    assert_examples(problem1)


@pytest.mark.parametrize("text,expected", [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 16384),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 16),
    ("????.######..#####. 1,6,5", 2500),
    ("?###???????? 3,2,1", 506250),
])
def test_problem2_detailed_examples(text, expected):
    assert problem2(text) == expected


def test_problem2_examples():
    assert_examples(problem2)
