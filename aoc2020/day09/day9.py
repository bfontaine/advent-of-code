from collections import deque


def read_numbers(filename):
    with open(filename) as f:
        return [int(line.strip()) for line in f]


def get_first_invalid_number(numbers, preamble_size=25):
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
                return number

        # 2. add the current number to the previous sums
        for offset, index_sums in enumerate(sums):
            prev_index = index - len(sums) + offset
            index_sums.add(numbers[prev_index] + number)

        sums.append(set())


def problem1(filename, preamble_size=25):
    print(get_first_invalid_number(read_numbers(filename), preamble_size))


def problem2(filename, preamble_size=25):
    numbers = read_numbers(filename)
    target = get_first_invalid_number(numbers, preamble_size)

    for i, n1 in enumerate(numbers):
        curr_sum = n1
        smallest = n1
        largest = n1
        for n2 in numbers[i + 1:]:
            curr_sum += n2
            if curr_sum > target:
                break

            if n2 < smallest:
                smallest = n2
            elif n2 > largest:
                largest = n2

            if curr_sum == target:
                print(sum([smallest, largest]))
                return


if __name__ == '__main__':
    # problem2("sample.txt", 5)
    problem2("input.txt")
