import std/unittest
from day04 import oneIsFullyContained, isOverlapping

test "fully contained":
  check(oneIsFullyContained([0, 1000], [100, 500]))
  check(oneIsFullyContained([0, 1000], [100, 1000]))
  check(oneIsFullyContained([0, 1000], [0, 1000]))
  check(oneIsFullyContained([0, 1000], [0, 1]))
  check(oneIsFullyContained([0, 9], [0, 10]))
  check(oneIsFullyContained([5, 6], [0, 10]))
  check(not oneIsFullyContained([5, 11], [0, 10]))

test "overlap":
  check(isOverlapping([0, 100], [100, 200]))
  check(isOverlapping([0, 100], [50, 200]))
  check(isOverlapping([0, 100], [0, 200]))
  check(isOverlapping([20, 100], [0, 200]))
  check(isOverlapping([100, 200], [0, 150]))
  check(isOverlapping([20, 30], [19, 29]))