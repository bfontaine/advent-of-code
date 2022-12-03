import os
import std/algorithm
import strutils

if paramCount() != 2:
  stderr.writeLine("Usage: <program> <problem number> <input file>")
  quit(QuitFailure)

let problemNumber = parseInt(paramStr(1))
let inputFile = paramStr(2)

if problemNumber != 1 and problemNumber != 2:
  stderr.writeLine("Problem number must be 1 or 2")
  quit(QuitFailure)

var currentElf = 0
var elves = newSeq[int](0)

for line in lines inputFile:
  if line == "":
    elves.add(currentElf)
    currentElf = 0
  else:
    currentElf += parseInt(line)

if currentElf != 0:
  elves.add(currentElf)

elves.sort(order=SortOrder.Descending)

if problemNumber == 1:
  echo elves[0]
else:
  echo elves[0] + elves[1] + elves[2]