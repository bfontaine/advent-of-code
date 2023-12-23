import re
from dataclasses import dataclass, field
from math import lcm
from typing import Tuple, Dict, List

import aoc


@dataclass
class Network:
    directions: List[int]
    nodes: Dict[str, Tuple[str, str]] = field(default_factory=dict)

    @classmethod
    def from_string(cls, s: str):
        directions_str, network_str = s.split('\n\n')
        network = cls(
            directions=[0 if d == "L" else 1 for d in directions_str],
        )

        for line in network_str.splitlines():
            origin, left, right = re.findall("[0-9A-Z]{3}", line)
            network.nodes[origin] = (left, right)

        return network

    def get_steps(self, node: str, ghost=False):
        steps = 0
        while not node.endswith("Z") if ghost else node != "ZZZ":
            for direction in self.directions:
                node = self.nodes[node][direction]
                steps += 1
        return steps


def problem1(text: str):
    network = Network.from_string(text)
    return network.get_steps("AAA")


def problem2(text: str):
    network = Network.from_string(text)

    initial_nodes = [node for node in network.nodes if node.endswith("A")]

    nodes_steps: List[int] = []
    for node in initial_nodes:
        node_steps = network.get_steps(node, ghost=True)
        if node_steps > 0:
            nodes_steps.append(node_steps)

    return lcm(*nodes_steps)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
