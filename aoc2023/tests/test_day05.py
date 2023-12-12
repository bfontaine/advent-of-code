from collections import OrderedDict

import pytest
from aocd.examples import Example

import day05
from day05 import CategoryMap, RangeAlmanac
from aoc import assert_examples, get_puzzle


def test_category_map():
    cm = CategoryMap()
    assert cm.convert(42) == 42
    cm.add_range_from_string("50 98 2")
    assert cm.convert(97) == 97
    assert cm.convert(98) == 50
    assert cm.convert(99) == 51
    assert cm.convert(100) == 100


@pytest.mark.parametrize("ranges,expected", [
    (
            {
                range(50, 60): range(0, 10),
            },
            [range(0, 50), range(0, 10), range(60, 100)]
    ),
    (
            {
                range(-10, 20): range(10, 40),
                range(48, 50): range(49, 51),
                range(90, 120): range(190, 220),
            },
            [range(20, 40), range(20, 48), range(49, 51), range(50, 90), range(190, 200)],
    ),
    (
            {range(0, 10): range(0, 10)},
            [range(0, 10), range(10, 100)],
    ),
    (
            {range(110, 120): range(10, 20)},
            [range(0, 100)],
    ),
    (
            {
                range(50, 98): range(52, 100),
                range(98, 100): range(50, 52),
            },
            [range(0, 50), range(52, 100), range(50, 52)],
    )
])
def test_convert_range(ranges, expected):
    r = range(0, 100)

    cm = CategoryMap(ranges=ranges)
    ls = list(cm.convert_range(r))
    assert ls == expected, f"CategoryMap({ranges}).convert_range({r}) should be {expected}"

    almanac = RangeAlmanac(seeds=[], category_maps=[cm])
    assert list(almanac.convert_ranges([r])) == expected


def test_convert_ranges_ordered():
    cm = CategoryMap(ranges=OrderedDict([(range(98, 100), range(50, 52)),
                                         (range(50, 98), range(52, 100))]))
    ls = list(cm.convert_range(range(80, 85)))
    assert ls == [range(82, 87)]


def test_range_almanac_from_string():
    text = ("seeds: 80 5\n"
            "seed-to-soil map:\n"
            "50 98 2\n"
            "52 50 48\n"
            "\n"
            "soil-to-fertilizer map:\n"
            "0 0 1")
    almanac = RangeAlmanac.from_string(text)
    assert almanac.seeds == [range(80, 85)]
    assert len(almanac.category_maps) == 2
    s2s = almanac.category_maps[0]
    assert s2s.ranges == {
        range(98, 98 + 2): range(50, 50 + 2),
        range(50, 50 + 48): range(52, 52 + 48),
    }
    s2t = almanac.category_maps[1]
    assert s2t.ranges == {
        range(0, 1): range(0, 1),
    }

    assert almanac.convert(82) == 84


def test_range_almanac_convert_ranges():
    almanac = RangeAlmanac(seeds=[], category_maps=[
        CategoryMap(ranges={
            range(50, 98): range(52, 100),
            range(98, 100): range(50, 52),
        }),
        # out of range
        CategoryMap(ranges={range(10, 20): range(10, 20)}),
        # identity
        CategoryMap(ranges={range(0, 100): range(0, 100)}),
    ])
    assert almanac.convert_ranges([range(82, 83), range(83, 84)]) \
           == [range(84, 85), range(85, 86)]


def test_problem1_examples():
    assert_examples(day05.problem1)


def test_problem2_reduced_example():
    example: Example = get_puzzle().examples[0]
    # > In the above example, the lowest location number can be obtained from seed number 82
    text = example.input_data.replace("seeds: 79 14 55 13", "seeds: 82 1")

    almanac = RangeAlmanac.from_string(text)
    assert almanac.seeds == [range(82, 83)]

    assert str(day05.problem2(text)) == example.answer_b


def test_problem2_examples():
    assert_examples(day05.problem2)
