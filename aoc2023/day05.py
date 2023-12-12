from dataclasses import field, dataclass
from typing import List, Dict, Optional, Generic, TypeVar

import aoc

T = TypeVar("T")


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

    def reverse(self):
        return CategoryMap(ranges={dest: origin for origin, dest in self.ranges.items()})


@dataclass
class Almanac(Generic[T]):
    seeds: List[T] = field(default_factory=list)
    category_maps: List[CategoryMap] = field(default_factory=list)

    def set_seeds_from_string(self, s: str):
        raise NotImplementedError()

    @classmethod
    def from_string(cls, s: str):
        almanac = cls()

        category_map: Optional[CategoryMap] = None

        for line in s.splitlines(keepends=False):
            if line.startswith("seeds:"):
                almanac.set_seeds_from_string(line)
                continue

            if ":" in line:
                category_map = CategoryMap()
                continue

            if category_map:
                if not line:
                    almanac.category_maps.append(category_map)
                    continue

                category_map.add_range_from_string(line)

        assert category_map is not None
        almanac.category_maps.append(category_map)
        return almanac

    def convert(self, n: int):
        for category_map in self.category_maps:
            n = category_map.convert(n)
        return n


@dataclass
class BasicAlmanac(Almanac[int]):
    """An almanac where seeds are simple numbers."""

    def set_seeds_from_string(self, s: str):
        self.seeds = [int(seed) for seed in s.replace("seeds: ", "").split(" ")]


@dataclass
class RangeAlmanac(Almanac[range]):
    """An almanac where seeds are written as ranges."""

    def set_seeds_from_string(self, s: str):
        # > The values on the initial seeds: line come in pairs.
        # > Within each pair, the first value is the start of the range and the second value is the length of the range.
        seed_range_bounds = [int(seed) for seed in s.replace("seeds: ", "").split(" ")]
        seed_range_pairs = [(seed_range_bounds[i], seed_range_bounds[i + 1])
                            for i in range(0, len(seed_range_bounds), 2)]
        self.seeds = [range(a, a + b) for a, b in seed_range_pairs]

    def has_seed(self, n: int):
        for r in self.seeds:
            if n in r:
                return True


def problem1(text: str):
    almanac = BasicAlmanac.from_string(text)
    location_numbers = [almanac.convert(seed) for seed in almanac.seeds]
    return min(location_numbers)


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
