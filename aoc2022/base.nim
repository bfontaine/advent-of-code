from os import paramStr, paramCount
from strutils import parseInt

type ProblemParams = tuple[problemNumber: int, inputFile: string]

proc problemParams*(): ProblemParams =
  if paramCount() != 2:
    stderr.writeLine("Usage: <program> <problem number> <input file>")
    quit(QuitFailure)

  let problemNumber = parseInt(paramStr(1))
  let inputFile = paramStr(2)

  if problemNumber != 1 and problemNumber != 2:
    stderr.writeLine("Problem number must be 1 or 2")
    quit(QuitFailure)

  return (problemNumber: problemNumber, inputFile: inputFile)
