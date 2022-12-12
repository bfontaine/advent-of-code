from "../base.nim" import problemParams

type
  PacketScanner* = ref object
    size: int
    buffer: seq[char]
    index: int


method add(self: PacketScanner, packet: char) =
  self.buffer.setLen(self.size)
  self.buffer[self.index] = packet
  self.index = (self.index + 1) mod self.size

method unique(self: PacketScanner): bool =
  # This method could be made more performant but it's fine for our scale
  var s: set[char]
  for c in self.buffer:
    if c in s:
      return false
    s.incl(c)
  return true

func startPacketPosition*(signal: string, size: int): int =
  var ps = PacketScanner(size: size)
  for i, c in signal:
    ps.add(c)
    if i >= 3 and ps.unique():
      return i+1
  return -1


if isMainModule:
  let
    params = problemParams()
    signal = readFile(params.inputFile)

  echo(startPacketPosition(signal, if params.problemNumber == 1: 4 else: 14))
