import std/sets
import std/strscans
import std/strutils
import tables
from "../base.nim" import problemParams

type Coord* = tuple[y: int, x: int]

let
  directions = {
    'U': (y: -1, x:  0),
    'D': (y: +1, x:  0),
    'L': (y:  0, x: -1),
    'R': (y:  0, x: +1),
  }.toTable


# can't use 'func' because the compiler says this can have side-effects
proc applyDirection*(cx: Coord, direction: char): Coord =
  let offsets = directions[direction]
  return (y: cx.y + offsets.y,
          x: cx.x + offsets.x)

func getOffset*(a: int, b: int): int =
  if a == b:
    return 0
  if a < b:
    return -1
  return 1

func isTouching*(c1: Coord, c2: Coord): bool =
  return abs(c1.x-c2.x) <= 1 and abs(c1.y-c2.y) <= 1

func moveTail*(head: Coord, tail: Coord): Coord =
  if isTouching(head, tail):
    return tail

  return (
    tail.y + getOffset(head.y, tail.y),
    tail.x + getOffset(head.x, tail.x)
  )

iterator parseLines(lines: seq[string]): (char, int) =
  var
    direction_string: string
    steps: int
    direction: char

  for line in lines:
    if line == "":
      break
    assert scanf(line, "$w $i", direction_string, steps) # $c doesn't work
    direction = direction_string[0]
    yield (direction, steps)


proc problem1*(lines: seq[string]): int =
  var
    head = (y: 0, x: 0)
    tail = (y: 0, x: 0)
    tailPositions = initHashSet[Coord]()

  tailPositions.incl(tail)

  for direction, steps in parseLines(lines):
    for _ in 1 .. steps:
      head = applyDirection(head, direction)

      tail = moveTail(head, tail)
      tailPositions.incl(tail)

  return len(tailPositions)


proc problem2*(lines: seq[string]): int =
  42 # TODO


if isMainModule:
  let
    params = problemParams()
    lines = readFile(params.inputFile).splitLines

  let fn = if params.problemNumber == 1: problem1 else: problem2
  echo(fn(lines))
