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

    def rotate(self, offset):
        if offset == 0:
            return

        self.x, self.y = self.y, -self.x
        self.rotate(offset - 1)


COMPASS = ["E", "S", "W", "N"]
DIRECTIONS = {
    "N": Coord(0, 1),
    "W": Coord(-1, 0),
    "S": Coord(0, -1),
    "E": Coord(1, 0),
}


def rotation_offset(action, arg):
    offset = arg // 90
    if action == "L":
        offset = -offset
    return (offset + 4) % 4


def problem1(actions):
    position = Coord(0, 0)

    direction_index = 0

    for action, arg in actions:
        # turn
        if action in {"L", "R"}:
            offset = rotation_offset(action, arg)
            direction_index = (direction_index + 4 + offset) % 4
            continue

        if action == "F":
            offsets = DIRECTIONS[COMPASS[direction_index]]
        else:
            offsets = DIRECTIONS[action]

        position.apply_offsets(offsets, arg)

    print(position.x, position.y, position.manhattan_distance())


def problem2(actions):
    position = Coord(0, 0)
    waypoint = Coord(10, 1)

    for action, arg in actions:
        # turn
        if action in {"L", "R"}:
            offset = rotation_offset(action, arg)
            waypoint.rotate(offset)
            continue

        if action == "F":
            position.apply_offsets(waypoint, arg)
            continue

        direction = DIRECTIONS[action]
        waypoint.apply_offsets(direction, arg)

    print(position.x, position.y, position.manhattan_distance())


if __name__ == '__main__':
    problem2(read_instructions("input.txt"))
