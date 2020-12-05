def decode(code, lower, upper, max_value):
    min_value = 0
    for char in code:
        middle = (min_value + max_value) // 2

        if char == lower:
            max_value = middle
        elif char == upper:
            min_value = middle + 1

    return min_value if code[-1] == upper else max_value


def decode_row(code):
    return decode(code, "F", "B", 127)


def decode_column(code):
    return decode(code, "L", "R", 7)


def decode_seat_id(code):
    row = decode_row(code[:7])
    column = decode_column(code[7:])
    return row * 8 + column


def read_seat_ids():
    with open("input.txt") as f:
        for line in f:
            yield decode_seat_id(line.strip())


def problem1():
    highest_seat_id = 0
    for seat_id in read_seat_ids():
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id

    print(highest_seat_id)


if __name__ == '__main__':
    problem1()
