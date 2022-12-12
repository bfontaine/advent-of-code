import std/unittest
from day06 import startPacketPosition

test "samples":
  check(startPacketPosition("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7)
  check(startPacketPosition("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5)
  check(startPacketPosition("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6)
  check(startPacketPosition("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10)
  check(startPacketPosition("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11)

  check(startPacketPosition("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19)
  check(startPacketPosition("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23)
  check(startPacketPosition("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23)
  check(startPacketPosition("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29)
  check(startPacketPosition("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26)
