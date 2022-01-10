# -*- coding: UTF-8 -*-

import sys
from typing import Tuple

class Packet:
    def __init__(self, version):
        self.version = version

    def versions_sum(self):
        return self.version


class LitteralPacket(Packet):
    def __init__(self, version, value):
        super().__init__(version)
        self.value = value

    def __repr__(self):
        return f"LP({self.version}):" + str(self.value)


class OperatorPacket(Packet):
    def __init__(self, version):
        super().__init__(version)
        self.subpackets = []

    def versions_sum(self):
        return self.version + sum(p.versions_sum() for p in self.subpackets)

    def __repr__(self):
        return f"OP({self.version}):" + repr(self.subpackets)


def parse_packet(b: str, start=0, end=-1) -> Tuple[Packet, int]:
    if end == -1:
        end = len(b)
    elif end > len(b):
        raise RuntimeError("end>len(b): " + str(end) + " > " + str(len(b)))

    # print("parsing", end - start)
    # print(b[:25])
    # print("VVVTTTI" + "L" * 15)
    #print(" " * start + "^" * (end - start))

    size = end - start

    version = int(b[start:start+3], 2)
    type_id = int(b[start+3:start+6], 2)
    last_bit = end

    # print("type id", type_id)

    if type_id == 4:
        bits = ""

        for i in range(start+6, end, 5):
            t = b[i]
            bits += b[i+1:i+5]
            last_bit = i+5
            if t == "0":
                break

        n = int(bits, 2)
        # print("litteral", n, "last bit", last_bit)
        return LitteralPacket(version, n), last_bit

    # 011 010 0 01010
    # VVV TTT I LLLL....
    # 012 345 6
    p = OperatorPacket(version)

    length_type_id = b[start+6]
    if length_type_id == "0":
        # print(" " * (start+7) + b[start+7:start+7+15])

        subpackets_length = int(b[start+7:start+7+15], 2)
        # print(subpackets_length, len(b))
        next_packet_index = start + 7 + 15
        max_index = next_packet_index + subpackets_length

        while next_packet_index < max_index:
            subpacket, next_packet_index = parse_packet(b, next_packet_index, max_index)
            p.subpackets.append(subpacket)
            # print(next_packet_index, max_index)
        return p, next_packet_index # maybe off-by-one error?

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

    # print(p)
    print(p.versions_sum())


if __name__ == "__main__":
    main()
