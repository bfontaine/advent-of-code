import re
from dataclasses import dataclass, field
from typing import Tuple, Dict

import aoc


@dataclass
class Network:
    nodes: Dict[str, Tuple[str, str]] = field(default_factory=dict)

    @classmethod
    def from_string(cls, s: str):
        network = cls()
        for line in s.splitlines(keepends=False):
            origin, left, right = re.findall("[A-Z]{3}", line)
            network.nodes[origin] = (left, right)
        return network

    def get_next_node(self, node: str, direction: str):
        node_neighbours = self.nodes[node]
        return node_neighbours[0] if direction == "L" else node_neighbours[1]


def parse_map(text: str) -> Tuple[str, Network]:
    instructions, network_str = text.split('\n\n')
    return instructions, Network.from_string(network_str)


def problem1(text: str):
    instructions, network = parse_map(text)

    node = "AAA"
    steps = 0
    while node != "ZZZ":
        for direction in instructions:
            node = network.get_next_node(node, direction)
            steps += 1

    return steps


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
