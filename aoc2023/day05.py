from dataclasses import field, dataclass
from typing import List, Dict, Optional

import aoc


@dataclass
class CategoryMap:
    ranges: Dict[range, range] = field(default_factory=dict)

    def convert(self, n: int):
        for range_from, range_to in self.ranges.items():
            if n in range_from:
                index = range_from.index(n)
                return range_to[index]
        # > Any source numbers that aren't mapped correspond to the same destination number.
        return n

    def add_range_from_string(self, s: str):
        # 50 98 2
        # > The first line has a destination range start of 50, a source range start of 98, and a range length of 2.
        dest_range_start, source_range_start, range_length = [int(n) for n in s.split(" ")]
        range_from = range(source_range_start, source_range_start + range_length)
        range_to = range(dest_range_start, dest_range_start + range_length)
        self.ranges[range_from] = range_to


@dataclass
class Almanac:
    seeds: List[int] = field(default_factory=list)
    category_maps: List[CategoryMap] = field(default_factory=list)

    @classmethod
    def from_string(cls, s: str):
        almanac = cls()

        category_map: Optional[CategoryMap] = None

        for line in s.splitlines(keepends=False):
            if line.startswith("seeds:"):
                almanac.seeds = [int(seed) for seed in line.replace("seeds: ", "").split(" ")]
                continue

            if ":" in line:
                category_map = CategoryMap()
                continue

            if category_map:
                if not line:
                    almanac.category_maps.append(category_map)
                    continue

                category_map.add_range_from_string(line)

        almanac.category_maps.append(category_map)
        return almanac

    def convert(self, n: int):
        for category_map in self.category_maps:
            n = category_map.convert(n)
        return n


def problem1(text: str):
    almanac = Almanac.from_string(text)
    location_numbers = [almanac.convert(seed) for seed in almanac.seeds]
    return min(location_numbers)


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
