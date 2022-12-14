import std/strscans
import std/strutils
from "../base.nim" import problemParams

iterator run*(lines: seq[string]): (int, int) =
  var
    register = 1
    cycles = 0

  for line in lines:
    if line == "":
      break

    cycles += 1
    yield (cycles, register)

    if line == "noop":
      continue

    var i: int
    assert scanf(line, "addx $i", i)

    cycles += 1
    yield (cycles, register)
    register += i


func interestingCycle(cycle: int): bool =
  return (cycle-20) mod 40 == 0 and cycle <= 220

proc problem1(lines: seq[string]) =
  var signal = 0

  for cycle, register in run(lines):
    if interestingCycle(cycle):
      signal += cycle*register

  echo(signal)

proc problem2(lines: seq[string]) =
  var
    row = ""
    i = 0

  for cycle, register in run(lines):
    let lit = abs(register - i) <= 1
    row &= (if lit: "#" else: " ")
    i += 1
    if cycle mod 40 == 0:
      echo(row)
      i = 0
      row = ""

    if cycle == 240:
      break


if isMainModule:
  let
    params = problemParams()
    lines = readFile(params.inputFile).splitLines
    fn = if params.problemNumber == 1: problem1 else: problem2

  fn(lines)
