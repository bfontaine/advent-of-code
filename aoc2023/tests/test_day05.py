import day05
from aoc import assert_examples


def test_category_map():
    cm = day05.CategoryMap()
    assert cm.convert(42) == 42
    cm.add_range_from_string("50 98 2")
    assert cm.convert(97) == 97
    assert cm.convert(98) == 50
    assert cm.convert(99) == 51
    assert cm.convert(100) == 100


def test_problem1_examples():
    assert_examples(day05.problem1)

# def test_problem2_examples():
#     assert_examples(day05.problem2)
