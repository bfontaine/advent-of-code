from collections import defaultdict


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


def problem1(indications):
    tiling = defaultdict(bool)

    for indication in indications:
        coordinates = coordinates_from_indication(indication)
        tiling[coordinates] = not tiling[coordinates]

    print(len([t for t in tiling.values() if t]))


if __name__ == '__main__':
    problem1(read_indications("input.txt"))
