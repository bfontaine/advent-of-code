import std/sets
from "../base.nim" import problemParams

let zeroCharValue = int('0')

func problem1(grid: seq[seq[int]], height: int, width: int): int =
  var
    visible = initHashSet[(int, int)]()
    highestTree: int

  proc checkTree(y: int, x: int) =
    let tree = grid[y][x]
    if tree > highestTree:
      visible.incl((y, x))
      highestTree = tree

  # for each row
  for y in countup(0, height-1):
    # from left
    highestTree = -1
    for x in countup(0, width-1):
      checkTree(y, x)

    # from right
    highestTree = -1
    for x in countdown(width-1, 0):
      checkTree(y, x)

  # for each column
  for x in countup(0, width-1):
    # from top
    highestTree = -1
    for y in countup(0, height-1):
      checkTree(y, x)

    # from bottom
    highestTree = -1
    for y in countdown(height-1, 0):
      checkTree(y, x)

  return len(visible)


func problem2(grid: seq[seq[int]], height: int, width: int): int =
  var
    highestScenicScore = 0
    scenicScore: int
    tree: int
    view: int

  # very bad time complexity but the input is small
  for y in 0 .. height-1:
    for x in 0 .. width-1:
      tree = grid[y][x]
      scenicScore = 1

      # This code would be a lot more easier to read/write if we had some sort
      # of 'takeWhile', e.g.:
      #
      #   ->> countdown(y-1, 0)
      #       takeWhile( y => grid[y][x] > tree )
      #       count

      # top
      view = 0
      for y1 in countdown(y-1, 0):
        view += 1
        if grid[y1][x] >= tree:
          break
      scenicScore *= view

      # bottom
      view = 0
      for y1 in countup(y+1, height-1):
        view += 1
        if grid[y1][x] >= tree:
          break
      scenicScore *= view

      # left
      view = 0
      for x1 in countdown(x-1, 0):
        view += 1
        if grid[y][x1] >= tree:
          break
      scenicScore *= view

      # right
      view = 0
      for x1 in countup(x+1, width-1):
        view += 1
        if grid[y][x1] >= tree:
          break
      scenicScore *= view

      if scenicScore > highestScenicScore:
        highestScenicScore = scenicScore

  # 5762400 is too high
  # 196 is too low
  return highestScenicScore


if isMainModule:
  let
    params = problemParams()
    zeroCharValue = int('0')

  var
    grid = newSeq[seq[int]](0)

  for line in lines params.inputFile:
    var row = newSeq[int](len(line))

    for x, c in line:
      let n = int(c) - zeroCharValue
      row[x] = n

    grid.add(row)

  let
    height = len(grid)
    width = len(grid[0])

  let fn = if params.problemNumber == 1: problem1 else: problem2
  echo(fn(grid, height, width))
