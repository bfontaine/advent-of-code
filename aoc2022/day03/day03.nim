import std/sets
from "../base.nim" import params

proc priority(c: char): int =
  let codePoint = int(c)
  # a (97) .. z -> 1 .. 26
  # A (65) .. Z -> 27 .. 52
  return codePoint - (if codePoint >= 97: 96 else: 38)

var totalPriority = 0

for line in lines params.inputFile:
  let
    compartment1 = toHashSet(line[0 .. int(line.len/2-1)])
    compartment2 = toHashSet(line[int(line.len/2) .. ^1])

  var intersection = (compartment1 * compartment2)
  let common = intersection.pop

  totalPriority += priority(common)

echo(totalPriority)
