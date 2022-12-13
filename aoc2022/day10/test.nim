import std/unittest
import day10

test "run":
  var cycles = newSeq[(int, int)](0)

  for cycle, register in run(@["noop", "addx 3", "addx -5"]):
    cycles.add((cycle, register))

  check(cycles == @[
    (1, 1), # > During the first cycle, X is 1
    (2, 1), # > During the second cycle, X is still 1
    (3, 1), # > During the third cycle, X is still 1
    (4, 4), # > During the fourth cycle, X is still 4.
    (5, 4), # > During the fifth cycle, X is still 4
    # (6, -1),
  ])
