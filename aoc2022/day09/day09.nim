import std/sets
import std/strscans
import std/strutils
import tables
from "../base.nim" import problemParams

type
  Coord* = tuple[y: int, x: int]
  Rope* = seq[Coord]

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


proc moveRopeKnots*(rope: var Rope) =
  for i in 0 .. rope.high-1:
    rope[i+1] = moveTail(rope[i], rope[i+1])


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


proc problemX(lines: seq[string], length: int): int =
  var
    rope = newSeq[Coord](length)
    tailPositions = initHashSet[Coord]()

  for i in 0 .. length-1:
    rope[i] = (y: 0, x: 0)

  tailPositions.incl(rope[rope.high])

  for direction, steps in parseLines(lines):
    for _ in 1 .. steps:
      rope[0] = applyDirection(rope[0], direction)
      moveRopeKnots(rope)
      tailPositions.incl(rope[rope.high])

  return len(tailPositions)


proc problem1*(lines: seq[string]): int =
  return problemX(lines, 2)


proc problem2*(lines: seq[string]): int =
  return problemX(lines, 10)


if isMainModule:
  let
    params = problemParams()
    lines = readFile(params.inputFile).splitLines

  let fn = if params.problemNumber == 1: problem1 else: problem2
  echo(fn(lines))
