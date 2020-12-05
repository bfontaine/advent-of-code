def problem1():
    left_offset = 0
    width = 0
    first = True
    trees = 0

    with open("input.txt") as f:
        for line in f:
            if first:
                width = len(line.strip())
                first = False
                continue

            left_offset = (left_offset + 3) % width
            position = line[left_offset]
            if position == "#":  # tree
                trees += 1

    print(trees)

if __name__ == '__main__':
    problem1()