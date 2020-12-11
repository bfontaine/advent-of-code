def read_seats(filename):
    # (x,y) -> int
    seats = {}
    with open(filename) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                if c == "L":
                    seats[(x, y)] = 0

    return seats


def adjacent_seats_occupancy(seats, x, y):
    n = 0
    for x1 in (x-1, x, x+1):
        for y1 in (y-1, y, y+1):
            if x1 == x and y1 == y:
                continue
            occupancy = seats.get((x1, y1))
            if occupancy is not None:
                n += occupancy

    return n


def next_seat_state(seats, x, y):
    occupied = seats[(x, y)]
    adjacent_occupancy = adjacent_seats_occupancy(seats, x, y)

    # "If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied."
    if not occupied and not adjacent_occupancy:
        return 1

    # "If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty."
    if occupied and adjacent_occupancy >= 4:
        return 0

    # "Otherwise, the seat's state does not change."
    return occupied


def next_round(seats):
    return {(x, y): next_seat_state(seats, x, y) for x, y in seats}


def problem1(filename):
    prev_seats = None
    seats = read_seats(filename)

    while prev_seats != seats:
        prev_seats = seats
        seats = next_round(seats)

    print(sum(seats.values()))


if __name__ == '__main__':
    problem1("input.txt")
