from collections import deque


def read_numbers(filename):
    with open(filename) as f:
        return [int(line.strip()) for line in f]


def problem1(filename, preamble_size=25):
    numbers = read_numbers(filename)

    sums = deque(maxlen=preamble_size)

    for index, number in enumerate(numbers):
        if index > preamble_size:
            # 1. if we're past the preamble, verify the number is correct
            found = False
            for s in sums:
                if number in s:
                    found = True
                    break

            if not found:
                print(number)
                break

        # 2. add the current number to the previous sums
        for offset, index_sums in enumerate(sums):
            prev_index = index - len(sums) + offset
            index_sums.add(numbers[prev_index] + number)

        sums.append(set())


if __name__ == '__main__':
    # problem1("sample.txt", 5)
    problem1("input.txt")
