def check_slope(x_direction, y_direction):
    left_offset = 0
    width = 0
    first = True
    trees = 0

    with open("input.txt") as f:
        for y, line in enumerate(f):
            if first:
                width = len(line.strip())
                first = False
                continue

            if y % y_direction != 0:
                continue

            left_offset = (left_offset + x_direction) % width
            position = line[left_offset]
            if position == "#":  # tree
                trees += 1

    return trees


def problem1():
    print(check_slope(3, 1))


def problem2():
    total = 1
    for x, y in (
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2),
    ):
        total *= check_slope(x, y)

    print(total)

if __name__ == '__main__':
    problem2()
