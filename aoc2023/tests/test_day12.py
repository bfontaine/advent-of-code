import json

import pytest

from aoc import assert_examples, get_input_data
from day12 import problem1, problem2, Record, _product


@pytest.mark.parametrize("record_str,expected1", [
    ("### 3", [0]),
    ("#??? 2", [0]),
    ("???? 4", [0]),
    ("???? 3", [0, 1]),
    ("???? 2", [0, 1, 2]),
    ("???? 1", [0, 1, 2, 3]),
    (".??? 1", [1, 2, 3]),
    ("..?? 1", [2, 3]),
    ("..?? 2", [2]),
    ("?? 2", [0]),
    ("?? 1", [0, 1]),
    ("??.. 2", [0]),
    ("??.. 1", [0, 1]),
])
def test_get_raw_possible_group_positions1(record_str, expected1):
    r = Record.from_string(record_str)
    assert r.get_raw_possible_group_positions() == [expected1]


@pytest.mark.parametrize("record_str,expected", [
    ("###?? 3,1", [[0], [4]]),
    ("??### 1,3", [[0], [2]]),
    ("???### 1,3", [[0, 1], [3]]),
    ("???.????? 3,1", [[0, 4], [4, 5, 6, 7, 8]]),
])
def test_get_raw_possible_group_positions2(record_str, expected):
    r = Record.from_string(record_str)
    assert r.get_raw_possible_group_positions() == expected


@pytest.mark.parametrize("record_str,expected", [
    # ??????#.???#????.???????#.???#????.
    # 0123456 89012345 78901234 678901234
    #           1           2         3
    ("??????#.???#????. 1,1,2,4,1",
     json.loads("""
     [[0, 1, 2, 3, 4],
            [2, 3, 4, 5, 6],
                  [4, 5,       8, 9],
                              [8, 9, 10, 11, 12],
                                                [13, 14, 15,     17],
                                                        [15,     17, 18, 19],
                                                                [17, 18, 19, 20, 21],
                                                                        [19, 20, 21, 22, 23],
                                                                                                    [26, 27, 28],
                                                                                                                        [31, 32, 33]]
     """)),
])
def test_get_possible_group_positions_fold2(record_str, expected):
    r = Record.from_string(record_str, folds=2)
    assert r.get_possible_group_positions() == expected


@pytest.mark.parametrize("record_str,expected", [
    ("???.??? 3", [[0, 4]]),
    ("???.??????? 1,4", [[0, 1, 2, 4, 5], [4, 5, 6, 7]]),
])
def test_get_possible_group_positions_unchanged_raw(record_str, expected):
    r = Record.from_string(record_str)
    assert r.get_raw_possible_group_positions() == expected
    assert r.get_possible_group_positions() == expected


"""
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
"""


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


@pytest.mark.parametrize("possible_positions,groups,expected", [
    ([[0, 1, 2, 3], [2, 3, 4]], [1, 1], [
        [0, 2], [0, 3], [0, 4],
        [1, 3], [1, 4],
        [2, 4]
    ]),
    ([[0, 1, 2], [3], [10]], [2, 5, 25], [
        [0, 3, 10]
    ]),
    ([[0, 1, 2, 3], [3, 4], [4, 5, 6, 7]], [3, 1, 1],
     [[0, 4, 6], [0, 4, 7]]),

    ([[0, 1, 2, 3], [3, 4], [4, 5, 6]], [2, 1, 1],
     [[0, 3, 5],
      [0, 3, 6],
      [0, 4, 6],
      [1, 4, 6]]),
])
def test_product(possible_positions, groups, expected):
    assert _product(possible_positions, groups) == expected


def test_problem1_examples():
    assert_examples(problem1)


def test_problem1_input():
    assert problem1(get_input_data()) == 7350


@pytest.mark.parametrize("text,expected", [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 16384),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
])
def test_problem2_detailed_examples(text, expected):
    assert problem2(text) == expected


def test_problem2_examples():
    assert_examples(problem2)


def test_problem2_input():
    assert problem2(get_input_data()) > 110121656453127  # > too low
