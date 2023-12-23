import pytest

from aoc import assert_examples
from day12 import problem1, problem2, Record


@pytest.mark.parametrize("record_str,expected", [
    ("### 3", range(0, 1)),
    ("#??? 2", range(0, 1)),
    ("???? 4", range(0, 1)),
    ("???? 3", range(0, 2)),
    ("???? 2", range(0, 3)),
    ("???? 1", range(0, 4)),
    (".??? 1", range(1, 4)),
    ("..?? 1", range(2, 4)),
    ("..?? 2", range(2, 3)),
    ("?? 2", range(0, 1)),
    ("?? 1", range(0, 2)),
    ("??.. 2", range(0, 1)),
    ("??.. 1", range(0, 2)),
])
def test_get_raw_possible_group_positions1(record_str, expected):
    r = Record.from_string(record_str)
    assert r.get_raw_possible_group_positions() == [expected]


@pytest.mark.parametrize("record_str,expected", [
    ("###?? 3,1", [range(0, 1), range(4, 5)]),
    ("??### 1,3", [range(0, 1), range(2, 3)]),
    ("???### 1,3", [range(0, 2), range(2, 4)]),
    ("???.????? 3,1", [range(0, 5), range(4, 9)]),
])
def test_get_raw_possible_group_positions2(record_str, expected):
    r = Record.from_string(record_str)
    assert r.get_raw_possible_group_positions() == expected


@pytest.mark.parametrize("record_str,expected_raw,expected", [
    ("???.??? 3", [range(0, 5)], [[0, 4]]),
])
def test_get_possible_group_positions(record_str, expected_raw, expected):
    r = Record.from_string(record_str)
    assert r.get_raw_possible_group_positions() == expected_raw
    assert r.get_possible_group_positions() == expected


@pytest.mark.parametrize("record_str,expected", [
    ("??? 1", [(0,), (1,), (2,)]),
    ("??? 1,1", [(0, 2)]),
    ("????? 2,2", [(0, 3)]),
    ("?????? 2,2", [(0, 3), (0, 4), (1, 4)]),
    ("#?? 1,1", [(0, 2)]),
    ("???.??? 3", [(0,), (4,)]),
    ("???.??? 2", [(0,), (1,), (4,), (5,)]),
    ("???.### 1,1,3", [(0, 2, 4)]),
    (".??..??...?##. 1,1,3", [(1, 5, 10), (1, 6, 10), (2, 5, 10), (2, 6, 10)]),

    ("?#?#?#?#?#?#?#? 1,3,1,6", [(1, 3, 7, 9)]),
    ("?#?#?#?#?#?#?#?.... 1,3,1,6", [(1, 3, 7, 9)]),
    ("?#.#?#?#?#?#?#? 1,3,1,6", [(1, 3, 7, 9)]),

    ("??##??##?? 2,2", [(2, 6)]),

    ("???.??????? 1,4",
     [(x, y)
      for x in (0, 1, 2)
      for y in (4, 5, 6, 7)] + [(4, 6), (4, 7), (5, 7)]),

    ("?????...#?? 5,1", [(0, 8)]),
    (".?#???..????#. 1,5", [(2, 8)]),
])
def test_get_possible_arrangements(record_str, expected):
    r = Record.from_string(record_str)
    assert sorted(r.get_possible_arrangements()) == expected


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




@pytest.mark.parametrize("record_str,expected,expected_folded5", [
    ("? 1", 1, 1),
    ("# 1", 1, 1),
    ("## 2", 1, 1),
    ("### 3", 1, 1),
    ("#. 1", 1, 1),
    (".# 1", 1, 1),

    ("???.### 1,1,3", 1, 1),
])
def test_count_possible_arrangements_folded(record_str, expected, expected_folded5):
    assert Record.from_string(record_str).count_possible_arrangements() == expected
    assert Record.from_string(record_str, folds=5).count_possible_arrangements() == expected_folded5


def test_problem1_examples():
    assert_examples(problem1)


@pytest.mark.parametrize("text,expected", [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 16384),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
])
def test_problem2_detailed_examples(text, expected):
    assert problem2(text) == expected


def test_problem2_examples():
    assert_examples(problem2)
