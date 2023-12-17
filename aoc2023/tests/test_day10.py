import clj
import pytest

from day10 import problem1, problem2, Position, Map, STARTING_TILE, GROUND, Orientation, NORTH, WEST, EAST, SOUTH
from aoc import assert_examples, get_input_data


@pytest.fixture()
def simple_sample1():
    return """
.....
.S-7.
.|.|.
.L-J.
.....
    """.strip()


def test_tile_equality():
    assert GROUND != STARTING_TILE


def test_position_equality():
    assert Position(10, 34) == Position(10, 34)


def test_starting_position(simple_sample1):
    m = Map.from_text(simple_sample1)
    assert m.starting_position == Position(1, 1)


def test_problem1_examples():
    assert_examples(problem1, examples=(0, 1))


@pytest.mark.parametrize("direction,orientation,expected", [
    (NORTH, Orientation.PORTSIDE, WEST),
    (NORTH, Orientation.STARBOARD, EAST),
    (SOUTH, Orientation.PORTSIDE, EAST),
    (SOUTH, Orientation.STARBOARD, WEST),
    (WEST, Orientation.PORTSIDE, SOUTH),
    (WEST, Orientation.STARBOARD, NORTH),
    (EAST, Orientation.PORTSIDE, NORTH),
    (EAST, Orientation.STARBOARD, SOUTH),
])
def test_get_direction_from_orientation(direction, orientation, expected):
    assert direction.get_direction_from_orientation(orientation) == expected


@pytest.mark.parametrize("text", [
    # even x odd
    """
......
.F--7.
.|..|.
.S--J.
......
""",
    # Note: ensure these don't have (1,1) on the edge
    # even x even
    "S--7\n|..|\n|..|\nL--J",
    # odd x even
    "S-7\n|.|\n|.|\nL-J",
    # odd x odd
    "S-7\n|.|\nL-J",
])
def test_iter_positions(text):
    text = text.strip()
    m = Map.from_text(text)
    positions = list(m.iter_positions())
    assert len(positions) == len(text.replace("\n", ""))

    edge_size = m.width * 2 + m.height * 2 - 4
    edge_positions = set(clj.take(edge_size, positions))
    assert Position(0, 0) in edge_positions
    assert Position(m.width - 1, m.height - 1) in edge_positions
    assert Position(1, 1) not in edge_positions


@pytest.mark.parametrize("text,expected", [
    ("S7\nLJ", 0),
    ("""
F----7
|FS-7|
||..||
LJ..LJ
""".strip(), 4),
])
def test_get_outside_positions(text, expected):
    assert len(Map.from_text(text).get_outside_positions()) == expected


@pytest.mark.parametrize("text", [
    # 4-tiles loop with different starting positions
    "S7\nLJ",
    "FS\nLJ",
    "F7\nSJ",
    "F7\nLS",

    """
    S-7
    L-J
    """,
    # inverted U
    """
    -F--S|
    -|F7|-
    JLJLJF
    """,
])
def test_problem2_simple_empty_loops(text):
    assert problem2(text.strip().replace(" ", "")) == 0


def test_problem2_empty_loop():
    text = """
F----7
|F---J
|L---7
|F---J
|L---7
L----J
    """.strip()

    for i, c in enumerate(text):
        if c == "\n":
            continue

        text_with_starting_position = text[:i] + "S" + text[i + 1:]
        assert problem2(text_with_starting_position) == 0


@pytest.mark.parametrize("text,expected", [
    (
            """
F----7
|F---J
||F--7
|||..|
|LJ..S
|F---J
|L---7
L----J
            """, 4),
])
def test_problem2_simple_loops(text, expected):
    assert problem2(text.strip().replace(" ", "")) == expected


@pytest.mark.parametrize("text,expected", [
    (
            """
            S-7
            |.|
            L-J
            """, 1),
    (
            """
            F--7
            |--|
            ||J|
            L-SJ
            """, 4),
    (
            # one inside tile with only edges on its side
            """
            ..F-S
            F-JFJ
            L7.L7
            FJF7|
            L-JLJ
            """, 1),
    (
            # tiles outside that don't touch the loop
            """
            ..........
            .S------7.
            .|F----7|.
            .||....||.
            .||....||.
            .||....||.
            .|L-7F-J|.
            .|..||..|.
            .L--JL--J.
            ..........
            """, 4),

    (
            # tiles inside that don't touch the loop
            """
            .........
            .F--S--7.
            .|.....|.
            .|.....|.
            .|.....|.
            .L-----J.
            """, 15),
])
def test_problem2(text, expected):
    assert problem2(text.strip().replace(" ", "")) == expected


def test_problem2_examples():
    assert_examples(problem2, examples=range(2, 4, 5))
