from std/algorithm import sort, SortOrder
from strutils import parseInt

from "../base.nim" import problemParams

let params = problemParams()
var
  currentElf = 0
  elves = newSeq[int](0)

for line in lines params.inputFile:
  if line == "":
    elves.add(currentElf)
    currentElf = 0
  else:
    currentElf += parseInt(line)

if currentElf != 0:
  elves.add(currentElf)

elves.sort(order=SortOrder.Descending)

if params.problemNumber == 1:
  echo elves[0]
else:
  echo elves[0] + elves[1] + elves[2]