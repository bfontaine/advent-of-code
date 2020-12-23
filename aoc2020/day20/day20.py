from collections import namedtuple, defaultdict, Counter
from functools import reduce
from typing import Tuple, Sequence, cast

import itertools
import math

Borders = namedtuple("Borders", ["top", "right", "bottom", "left"])


def parse_tile(tile_string: str):
    title, tile = tile_string.split("\n", maxsplit=1)
    tile_id = int(title[len("Tile "):-1])
    return tile_id, tile


def read_tiles(filename) -> Sequence[Tuple[int, str]]:
    with open(filename) as f:
        tile_strings = f.read().strip().split("\n\n")

    return [parse_tile(tile_string) for tile_string in tile_strings]


def get_tile_borders(tile: str) -> Borders:
    lines = tile.splitlines()
    top = lines[0]
    bottom = lines[-1]
    left = "".join([line[0] for line in lines])
    right = "".join([line[-1] for line in lines])
    return Borders(top, right, bottom, left)


def reverse_str(s: str):
    return "".join(reversed(s))


def rotate_right(borders: Borders) -> Borders:
    return Borders(
        reverse_str(borders.left),
        borders.top,
        reverse_str(borders.right),
        borders.bottom,
    )


def vertical_flip(borders: Borders) -> Borders:
    return Borders(
        borders.bottom,
        borders.right,
        borders.top,
        borders.left,
    )


def horizontal_flip(borders: Borders) -> Borders:
    return Borders(
        borders.top,
        borders.left,
        borders.bottom,
        borders.right,
    )


def tile_borders_permutations(tile_borders: Borders):
    # "each image tile has been rotated and flipped to a random orientation"

    #   T             L    B    R
    #  L R -rotate-> B T  R L  T B
    #   B             R    T    L
    #   |             |    |    |
    #  flip----.     ...  ...  ...
    #   |      |
    #   B      T
    #  L R    R L -> ...
    #   T      B
    #   |      |
    #  ...    ...
    permutations = set()

    permutation = tile_borders

    for _ in range(3):
        permutation = rotate_right(permutation)
        permutations.add(permutation)
        permutations.add(vertical_flip(permutation))
        permutations.add(horizontal_flip(permutation))

    return permutations


def problem1(tiles):
    # Faster than bruteforce everything: try only the corners

    matched_borders = defaultdict(set)

    for title, tile in tiles:
        borders_permutations = tile_borders_permutations(get_tile_borders(tile))
        for borders in borders_permutations:
            for border in borders:
                matched_borders[border].add(title)

    alone = Counter()

    for titles in matched_borders.values():
        if len(titles) == 1:
            alone[titles.pop()] += 1

    # values are doubled: 4 = corners, 2 = sides
    corners = [title for title in alone if alone[title] == 4]

    print(corners, reduce(lambda a, b: a * b, corners, 1))


if __name__ == '__main__':
    problem1(read_tiles("input.txt"))
