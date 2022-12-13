import std/unittest
from day09 import applyDirection, moveTail, getOffset, isTouching, Coord

test "applyDirection":
  check(applyDirection((3, 3), 'U') == (2, 3))
  check(applyDirection((3, 3), 'D') == (4, 3))
  check(applyDirection((3, 3), 'L') == (3, 2))
  check(applyDirection((3, 3), 'R') == (3, 4))

test "getOffset":
  check(getOffset(0, 0) == 0)
  check(getOffset(2, 5) == -1)
  check(getOffset(3, 1) == 1)
  check(getOffset(2, 0) == 1)

test "isTouching":
  for y in -1 .. +1:
    for x in -1 .. +1:
      check(isTouching((y, x), (0, 0)))
      check(isTouching((0, 0), (y, x)))

  check(not isTouching((0, 2), (0, 0)))


test "moveTail":
  # touching
  for y in -1 .. +1:
    for x in -1 .. +1:
      check(moveTail((0, 0), (y, x)) == (y, x))
      check(moveTail((y, x), (0, 0)) == (0, 0))

  # orthogonal moves
  check(moveTail((0, +2), (0, 0)) == (0, +1))
  check(moveTail((0, -2), (0, 0)) == (0, -1))
  check(moveTail((+2, 0), (0, 0)) == (+1, 0))
  check(moveTail((-2, 0), (0, 0)) == (-1, 0))

  # diagonals
  #  0123
  # 0..hh   for any of these head (h) positions,
  # 1..xh < the tail (t) moves in the x position.
  # 2.t..
  check(moveTail((2, 0), (1, 2)) == (2, 1))
  check(moveTail((3, 0), (1, 2)) == (2, 1))
  check(moveTail((3, 1), (1, 2)) == (2, 1))

  func distance(c1: Coord, c2: Coord): int =
    return abs(c1.y - c2.y) + abs(c1.x - c2.x)

  # everything: ensure the new distance is always smaller or equal
  for hy in 0 .. 20:
    for hx in 0 .. 20:
      for ty in 0 .. 20:
        for tx in 0 .. 20:
          let
            head = (hy, hx)
            tail1 = (ty, tx)
            tail2 = moveTail(head, tail1)

          check( distance(head, tail2) <= distance(head, tail1) )
