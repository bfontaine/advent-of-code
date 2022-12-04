from strutils import split

from "../base.nim" import problemParams

discard """
> A for Rock, B for Paper, and C for Scissors
> X for Rock, Y for Paper, and Z for Scissors

> The score for a single round is the score for the shape you selected
> (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round
> (0 if you lost, 3 if the round was a draw, and 6 if you won).
"""

type
  Shape = int8
  Result = int8

const
  # Add 1 here since we removed 1 from the Rock/Paper/Scissors values
  LossScore = 0 + 1
  DrawScore = 3 + 1
  WinScore = 6 + 1

  Rock: Shape = 0
  Paper: Shape = 1
  Scissors: Shape = 2

  # > X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.
  Loss: Result = 0
  Draw: Result = 1
  Win: Result = 2

proc parseShape(x: string): Shape =
  case x
  of "A", "X":
    return Rock
  of "B", "Y":
    return Paper
  of "C", "Z":
    return Scissors
  else:
    assert false

proc parseResult(x: string): Result =
  # here we use the fact that results have the same values as shapes
  parseShape(x)

proc score1(opponent: string, you: string): int =
  let
    opponentShape = parseShape(opponent)
    yourShape = parseShape(you)

  if opponentShape == yourShape:
    return yourShape + DrawScore
  if (opponentShape+1) mod 3 == yourShape:
    return yourShape + WinScore
  return yourShape + LossScore

proc score2(opponent: string, you: string): int =
  let
    opponentShape = parseShape(opponent)
    result = parseResult(you)

  case result
  of Win:
    return (opponentShape+1) mod 3 + WinScore
  of Draw:
    return opponentShape + DrawScore
  of Loss:
    return (opponentShape+2) mod 3 + LossScore
  else:
    assert false

let params = problemParams()

proc lineScore(line: string): int =
  let words = line.split(" ")
  assert len(words) == 2
  return (if params.problemNumber == 1: score1 else: score2)(words[0], words[1])

var totalScore = 0

for line in lines params.inputFile:
  totalScore += lineScore(line)

echo(totalScore)
