from collections import Counter, defaultdict


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


def problem2(filename):
    adapters = read_adapters(filename)
    max_adapter = adapters[-1]
    builtin_adapter = max_adapter + 3

    steps = [0] + adapters + [builtin_adapter]
    max_index = len(steps) - 1

    # index -> #
    paths = {}

    def compute_paths(index):
        if index in paths:
            return paths[index]

        # builtin adapter
        if index == max_index:
            return 1

        a = steps[index]
        paths_count = 0
        for offset, b in enumerate(steps[index + 1:]):
            if b > a + 3:
                break

            j = index + 1 + offset
            if j not in paths:
                paths[j] = compute_paths(j)

            paths_count += paths[j]

        paths[index] = paths_count
        return paths_count

    print(compute_paths(0))


if __name__ == '__main__':
    problem2("input.txt")
