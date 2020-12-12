def read_instructions(filename):
    with open(filename) as f:
        for line in f:
            action = line[0]
            arg = int(line[1:].strip())
            yield action, arg


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def apply_offsets(self, c, factor=1):
        self.x += c.x * factor
        self.y += c.y * factor

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


def problem1(actions):
    position = Coord(0, 0)

    compass = ["E", "S", "W", "N"]
    directions = {
        "N": Coord(0, 1),
        "S": Coord(0, -1),
        "W": Coord(-1, 0),
        "E": Coord(1, 0),
    }
    direction_index = 0

    for action, arg in actions:
        # turn
        if action in {"L", "R"}:
            offset = arg // 90
            if action == "L":
                offset = -offset
            direction_index = (direction_index + 4 + offset) % 4
            continue

        if action == "F":
            offsets = directions[compass[direction_index]]
        else:
            offsets = directions[action]

        position.apply_offsets(offsets, arg)

    print(position.x, position.y, position.manhattan_distance())


if __name__ == '__main__':
    problem1(read_instructions("input.txt"))
