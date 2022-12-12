import std/unittest
from day06 import startPacketPosition

test "samples":
  check(startPacketPosition("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7)
  check(startPacketPosition("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5)
  check(startPacketPosition("nppdvjthqldpwncqszvftbrmjlhg") == 6)
  check(startPacketPosition("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10)
  check(startPacketPosition("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11)
