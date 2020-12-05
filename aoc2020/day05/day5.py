from collections import defaultdict

ROW_WIDTH = 8


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
    return decode(code, "L", "R", ROW_WIDTH - 1)


def decode_seat(code):
    row = decode_row(code[:ROW_WIDTH - 1])
    column = decode_column(code[ROW_WIDTH - 1:])
    return row, column


def read_seats():
    with open("input.txt") as f:
        for line in f:
            yield decode_seat(line.strip())


def get_seat_id(row, column):
    return row * ROW_WIDTH + column


def problem1():
    highest_seat_id = 0
    for row, column in read_seats():
        seat_id = get_seat_id(row, column)

        if seat_id > highest_seat_id:
            highest_seat_id = seat_id

    print(highest_seat_id)


def problem2():
    rows = defaultdict(list)

    for row, column in read_seats():
        rows[row].append(column)

    for row_id, row in rows.items():
        if len(row) == ROW_WIDTH:
            continue

        if len(rows.get(row_id + 1, [])) != ROW_WIDTH or \
                len(rows.get(row_id - 1, [])) != ROW_WIDTH:
            continue

        column = list(set(range(ROW_WIDTH)) - set(row))[0]
        print(row_id, column, get_seat_id(row_id, column))
        break


if __name__ == '__main__':
    problem2()
