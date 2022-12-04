from strutils import split, parseInt
from "../base.nim" import params

var fully_contained_pairs = 0

for line in lines params.inputFile:
  let
    words = line.split({',', '-'})
    pair1 = [parseInt(words[0]), parseInt(words[1])]
    pair2 = [parseInt(words[2]), parseInt(words[3])]

  if params.problemNumber == 1:
    if pair1[0] <= pair2[0] and pair2[1] <= pair1[1] or
       pair2[0] <= pair1[0] and pair1[1] <= pair2[1]:
      fully_contained_pairs += 1
  # else:
  #   if pair1[0] <= pair2[0] and pair1[1]

echo(fully_contained_pairs)