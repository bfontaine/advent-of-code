from collections import Counter


def read_adapters(filename):
    with open(filename) as f:
        return sorted([int(line.strip()) for line in f])


def problem1(filename):
    adapters = read_adapters(filename)

    diff_counts = Counter()
    previous = 0

    for adapter in adapters:
        diff_counts[adapter - previous] += 1
        previous = adapter

    # last one
    diff_counts[3] += 1

    print(diff_counts[1], diff_counts[3], diff_counts[1] * diff_counts[3])


if __name__ == '__main__':
    problem1("input.txt")
