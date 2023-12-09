import aoc


def get_card_points(line: str):
    card_content = line.split(":", 1)[1]
    numbers_parts = card_content.split("|", 1)
    winning_numbers, card_numbers = [
        set(map(int, numbers.strip().split()))
        for numbers in numbers_parts
    ]
    matches = len(winning_numbers & card_numbers)
    if not matches:
        return 0

    return 2 ** (matches - 1)


def problem1(text: str):
    s = 0
    for line in text.splitlines():
        s += get_card_points(line)

    return s


if __name__ == '__main__':
    aoc.run(problem1)  # , problem2)
