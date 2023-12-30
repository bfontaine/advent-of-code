from aoc.containers import StringGrid


def test_string_grid_copy():
    g1 = StringGrid(rows=["foo", "bar"])
    g2 = g1.copy()
    assert g1 is not g2
    assert g2 is not g1
    assert g1 == g2
