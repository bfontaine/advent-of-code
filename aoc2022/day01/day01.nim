import os
import strutils

if paramCount() != 1:
  stderr.writeLine("Usage: <program> <input file>")
  quit(QuitFailure)

let inputFile = paramStr(1)

var currentElf = 0
var maxElf = 0

for line in lines inputFile:
  if line == "":
    maxElf = max(maxElf, currentElf)
    currentElf = 0
  else:
    currentElf += parseInt(line)

echo maxElf
