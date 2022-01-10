import sys
import math
from typing import Tuple


OPS = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda pp: int(pp[0] > pp[1]),
    6: lambda pp: int(pp[0] < pp[1]),
    7: lambda pp: int(pp[0] == pp[1]),
}

class Packet:
    def __init__(self, version):
        self.version = version

    def value(self):
        raise NotImplementedError()

    def versions_sum(self):
        return self.version


class LitteralPacket(Packet):
    def __init__(self, version, value):
        super().__init__(version)
        self._value = value

    def value(self):
        return self._value

    def __repr__(self):
        return f"LP({self.version}):" + str(self.value)


class OperatorPacket(Packet):
    def __init__(self, version, type_id):
        super().__init__(version)
        self.type_id = type_id
        self.subpackets = []

    def versions_sum(self):
        return self.version + sum(p.versions_sum() for p in self.subpackets)

    def value(self):
        return OPS[self.type_id]([p.value() for p in self.subpackets])

    def __repr__(self):
        return f"OP({self.version}):" + repr(self.subpackets)


def parse_packet(b: str, start=0, end=-1) -> Tuple[Packet, int]:
    if end == -1:
        end = len(b)
    elif end > len(b):
        raise RuntimeError("end>len(b): " + str(end) + " > " + str(len(b)))

    size = end - start

    version = int(b[start:start+3], 2)
    type_id = int(b[start+3:start+6], 2)
    last_bit = end

    if type_id == 4:
        bits = ""

        for i in range(start+6, end, 5):
            t = b[i]
            bits += b[i+1:i+5]
            last_bit = i+5
            if t == "0":
                break

        n = int(bits, 2)
        return LitteralPacket(version, n), last_bit

    p = OperatorPacket(version, type_id)

    length_type_id = b[start+6]
    if length_type_id == "0":

        subpackets_length = int(b[start+7:start+7+15], 2)
        next_packet_index = start + 7 + 15
        max_index = next_packet_index + subpackets_length

        while next_packet_index < max_index:
            subpacket, next_packet_index = parse_packet(b, next_packet_index, max_index)
            p.subpackets.append(subpacket)
        return p, next_packet_index

    else:
        subpackets_count = int(b[start+7:start+7+11], 2)
        next_packet_index = start + 7 + 11

        while subpackets_count:
            subpacket, next_packet_index = parse_packet(b, next_packet_index, end)
            subpackets_count -= 1
            p.subpackets.append(subpacket)

        return p, next_packet_index


def main():
    s = sys.stdin.read()
    h = int(s, 16)
    b = f"{h:b}"

    expected_size = 4 * len(s)
    b = "0" * (expected_size - len(b)) + b

    p, _ = parse_packet(b)

    print("Part 1:", p.versions_sum())
    print("Part 2:", p.value())


if __name__ == "__main__":
    main()
