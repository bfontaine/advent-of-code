import std/sets
from "../base.nim" import params

type RuckSack = HashSet[char]

proc priority(c: char): int =
  let codePoint = int(c)
  # a (97) .. z -> 1 .. 26
  # A (65) .. Z -> 27 .. 52
  return codePoint - (if codePoint >= 97: 96 else: 38)

var totalPriority = 0

var
  rucksacks: array[0..2, RuckSack]
  ruckSackIndex = 0

for line in lines params.inputFile:
  if params.problemNumber == 1:
    let
      compartment1: RuckSack = toHashSet(line[0 .. int(line.len/2-1)])
      compartment2: RuckSack = toHashSet(line[int(line.len/2) .. ^1])

    var intersection = (compartment1 * compartment2)
    let common = intersection.pop

    totalPriority += priority(common)
  else:
    rucksacks[ruckSackIndex] = toHashSet(line)
    if ruckSackIndex == 2:
      var intersection = (rucksacks[0] * rucksacks[1] * rucksacks[2])
      let common = intersection.pop

      ruckSackIndex = 0
      totalPriority += priority(common)
    else:
      ruckSackIndex += 1

echo(totalPriority)
