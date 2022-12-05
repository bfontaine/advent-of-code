from std/algorithm import reverse
from std/strscans import scanf
from sequtils import concat
from "../base.nim" import problemParams

if isMainModule:
  let params = problemParams()
  var
    stacks = newSeq[seq[char]](0)
    stacksParsing = true

  for line in lines params.inputFile:
    if len(line) > 0 and line[1] != '1':
      case line[0]:
        of '[', ' ':
          assert stacksParsing
          # [x] [y] ... -> each stack takes 4 chars except the last one
          # which takes 3 chars
          let stacksCount = int((len(line)+1) / 4)
          if len(stacks) < stacksCount:
            stacks.setLen(stacksCount)

          for i in 0..<stacksCount:
            let crate = line[1 + i*4]
            if crate != ' ':
              stacks[i].add(crate)
        of 'm':
          var craneCount, posFrom, posTo: int
          assert scanf(line, "move $i from $i to $i", craneCount, posFrom, posTo)

          # AFAIU I can't use this because stackFrom is a copy of stacks[posFrom-1]
          #  instead of a pointer to it??
          # var
          #   stackFrom = stacks[posFrom-1]
          #   stackTo = stacks[posTo-1]

          if params.problemNumber == 1:
            for _ in 0..<craneCount:
              let topCrane = stacks[posFrom-1][^1]
              stacks[posTo-1].add(topCrane)
              stacks[posFrom-1].delete(stacks[posFrom-1].high)
          else:
            var
              stackFrom = stacks[posFrom-1]
              stackTo = stacks[posTo-1]
            let topCranes = stackFrom[^craneCount..^1]
            stacks[posFrom-1] = stackFrom[0..^(craneCount+1)]
            stacks[posTo-1] = stacks[posTo-1].concat(topCranes)

          #for stack in stacks:
          #  echo stack
        else:
          continue
    else:
      # end of stacks
      if stacksParsing:
        for stack in stacks.mitems:
          reverse(stack)
          #echo stack
        stacksParsing = false

  var tops = ""
  for stack in stacks:
    tops &= stack[stack.high]
  echo tops
