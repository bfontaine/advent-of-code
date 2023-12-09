import day03
from aoc import assert_examples


def test_grid():
    g = day03.Grid.from_string(
        """
        ..123..
        .....*.
        456....
        """.strip().replace(" ", "")
    )

    assert g.height == 3
    assert g.width == 7

    assert g[0, 0] == "."
    assert g[1, 0] == "."
    assert g[2, 0] == "1"
    assert g[1, 1] == "."
    assert g[5, 1] == "*"
    assert g[0, 2] == "4"

    print(repr(g.text[7 + 5:]))


def test_problem1_examples():
    assert_examples(day03.problem1)

# def test_problem2_examples():
#     assert_examples(day03.problem2)
