from collections import defaultdict
from typing import Dict, Tuple, Collection, Set


def parse_indication(text):
    i = 0
    while i < len(text):
        if text[i] in {"n", "s"}:
            yield text[i] + text[i + 1]
            i += 2
        else:
            yield text[i]
            i += 1


def read_indications(filename):
    with open(filename) as f:
        for line in f:
            yield parse_indication(line.strip())


def coordinates_from_indication(indication):
    y = 0
    x = 0

    """
        xx NW xx
         W xx NE
        xx [] xx
        SW xx E
        xx SE xx
    """

    for direction in indication:
        if direction == "nw":
            y -= 2
        elif direction == "ne":
            y -= 1
            x += 1
        elif direction == "e":
            y += 1
            x += 1
        elif direction == "se":
            y += 2
        elif direction == "sw":
            y += 1
            x -= 1
        elif direction == "w":
            y -= 1
            x -= 1

    return x, y


def neighbor_coordinates(coordinates):
    x, y = coordinates
    return (
        (x, y - 2),
        (x + 1, y - 1),
        (x + 1, y + 1),
        (x, y + 2),
        (x - 1, y + 1),
        (x - 1, y - 1),
    )


Coordinates = Tuple[int, int]
Tiling = Dict[Coordinates, bool]


def next_tiling(tiling: Tiling) -> Tiling:
    coordinates_to_check: Set[Coordinates] = set()
    neighbors: Dict[Coordinates, Collection[Coordinates]] = {}

    new_tiling = defaultdict(bool)

    for coordinates in tiling:
        neighbors[coordinates] = neighbor_coordinates(coordinates)
        coordinates_to_check.add(coordinates)
        coordinates_to_check.update(neighbors[coordinates])

    for coordinates in coordinates_to_check:
        this_neighbors: Collection[Coordinates] = neighbors.get(coordinates) or neighbor_coordinates(coordinates)
        black_neighbors = len([n for n in this_neighbors if tiling.get(n)])
        black = tiling.get(coordinates)
        if black:
            if black_neighbors > 2 or not black_neighbors:
                continue  # flip to white
            # keep it
            new_tiling[coordinates] = True
        else:
            if black_neighbors == 2:
                new_tiling[coordinates] = True  # flip to black

            # otherwise: keep it

    return new_tiling


def count_black_tiles(tiling):
    return len([t for t in tiling.values() if t])


def run(indications):
    tiling = defaultdict(bool)

    for indication in indications:
        coordinates = coordinates_from_indication(indication)
        tiling[coordinates] = not tiling[coordinates]

    print("Problem #1:", count_black_tiles(tiling))

    for i in range(100):
        tiling = next_tiling(tiling)

    print("Problem #2:", count_black_tiles(tiling))


if __name__ == '__main__':
    run(read_indications("input.txt"))
