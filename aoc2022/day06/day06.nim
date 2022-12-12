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
  var s: set[char]
  for c in self.buffer:
    if c in s:
      return false
    s.incl(c)
  return true

func startPacketPosition*(signal: string): int =
  var ps = PacketScanner(size: 4)
  for i, c in signal:
    ps.add(c)
    if i >= 3 and ps.unique():
      return i+1
  return -1


if isMainModule:
  let
    params = problemParams()
    signal = readFile(params.inputFile)

  echo(startPacketPosition(signal))
