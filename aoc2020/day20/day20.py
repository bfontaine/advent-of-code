from collections import namedtuple, defaultdict
from functools import reduce
from typing import Tuple, Sequence

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


def problem1(tiles):
    # Faster than bruteforce everything: try only the corners
    # This works because the input is nice enough: every possible border matches only twice (between two squares)

    matched_borders = defaultdict(set)

    for title, tile in tiles:
        borders = get_tile_borders(tile)
        for border in borders:
            # don't even try the rotate/flip thing: adding each border and its reversed version is enough
            matched_borders[border].add(title)
            matched_borders[reverse_str(border)].add(title)

    edges = defaultdict(set)

    for border, titles in matched_borders.items():
        if len(titles) == 2:
            t1, t2 = list(titles)
            edges[t1].add(t2)
            edges[t2].add(t1)

    corners = [title for title, neighbors in edges.items() if len(neighbors) == 2]

    print("Problem #1:", corners, reduce(lambda a, b: a * b, corners, 1))


if __name__ == '__main__':
    problem1(read_tiles("sample.txt"))
    problem1(read_tiles("input.txt"))
