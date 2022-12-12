import tables
import future
import algorithm
import std/strutils
from "../base.nim" import problemParams

func joinPath(path: seq[string]): string =
  return path.join("/")

func joinPath(path: seq[string], trailing: string): string =
  if len(path) == 0:
    return trailing
  return path.join("/") & "/" & trailing

func getSizes(lines: seq[string]): int =
  var
    parentDirs = initTable[string, string]()
    sizes = initTable[string, int]()
    currDir = newSeq[string](0)

  for line in lines:
    if len(line) == 0:
      continue

    case line[0]:
      of '$':
        let
          words = line.split(" ")
          cmd = words[1]
          args = words[2..words.high]

        case cmd:
          of "cd":
            case args[0]:
              of "..":
                currDir.delete(currDir.high)
              of "/":
                currDir.setLen(0)
              else:
                currDir.add(args[0])
          of "ls":
            let path = joinPath(currDir)
            if not (path in sizes):
              sizes[path] = 0

      of 'd':
        # ls listing: directory
        let dirName = line.split(" ")[1]
        parentDirs[joinPath(currDir, dirName)] = joinPath(currDir)

      else:
        # ls listing: file
        let fileSize = line.split(" ")[0]
        sizes.mgetOrPut(joinPath(currDir), 0) += parseInt(fileSize)

  var dirs: seq[string]

  for dir in sizes.keys:
    dirs.add(dir)

  dirs.sort((a, b) => cmp(b.count("/"), a.count("/")))
  for dir in dirs:
    if dir in parentDirs:
      let parent = parentDirs[dir]
      sizes[parent] += sizes[dir]

  var totalSize = 0

  for size in sizes.values:
    if size < 100000:
      totalSize += size

  return totalSize


proc linesSeq(filename: string): seq[string] =
  var s: seq[string]
  for line in lines filename:
    s.add(line)
  return s


if isMainModule:
  let
    params = problemParams()

  echo(getSizes(linesSeq(params.inputFile)))
