from strutils import split, parseInt
from "../base.nim" import problemParams

type Pair = array[0..1, int]

proc oneIsFullyContained*(pair1: Pair, pair2: Pair): bool =
  return pair1[0] <= pair2[0] and pair2[1] <= pair1[1] or
         pair2[0] <= pair1[0] and pair1[1] <= pair2[1]

proc isOverlapping*(pair1: Pair, pair2: Pair): bool =
  return pair1[0] <= pair2[0] and pair2[0] <= pair1[1] or
         pair2[0] <= pair1[0] and pair1[0] <= pair2[1]

if isMainModule:
  let params = problemParams()
  var fully_contained_pairs = 0

  for line in lines params.inputFile:
    let
      words = line.split({',', '-'})
      pair1 = [parseInt(words[0]), parseInt(words[1])]
      pair2 = [parseInt(words[2]), parseInt(words[3])]

    if params.problemNumber == 1:
      fully_contained_pairs += int(oneIsFullyContained(pair1, pair2))
    else:
      fully_contained_pairs += int(isOverlapping(pair1, pair2))

  echo(fully_contained_pairs)