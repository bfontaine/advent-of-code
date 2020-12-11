class Seats:
    def __init__(self, filename, problem=1):
        self.rules = problem
        # (x, y) -> int
        self._seats = {}
        # (x, y) -> [(x, y), ...]
        self._views = {}

        self.height = 0
        self.width = 0

        with open(filename) as f:
            for y, line in enumerate(f):
                line = line.strip()
                self.height += 1
                self.width = len(line)

                for x, c in enumerate(line):
                    if c == "L":
                        self._seats[(x, y)] = 0

        self._compile_views()

    def _compile_views(self):
        # compute the views only once at the beginning
        directions = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if not dx == dy == 0]

        for x, y in self._seats:
            view = []

            if self.rules == 1:
                for dx, dy in directions:
                    x1y1 = (x + dx, y + dy)

                    if x1y1 in self._seats:
                        view.append(x1y1)
            else:
                # there's probably a better solution than doing that for every coordinate, but it's fast enough.
                for dx, dy in directions:
                    x1 = x+dx
                    y1 = y+dy

                    while 0 <= x1 < self.width and 0 <= y1 < self.height:
                        if (x1, y1) in self._seats:
                            view.append((x1, y1))
                            break

                        x1 += dx
                        y1 += dy

            self._views[(x, y)] = view

    def next_seat_state(self, x, y):
        occupied = self._seats.get((x, y))
        adjacent_occupancy = sum([self._seats[xy] for xy in self._views[(x, y)]])

        # "If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied."
        if not occupied:
            if not adjacent_occupancy:
                return 1
        else:
            min_adjacent_occupancy = 4 if self.rules == 1 else 5
            # 1: "If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat
            #     becomes empty."
            # 2: "it now takes five or more visible occupied seats for an occupied seat to become empty"
            if adjacent_occupancy >= min_adjacent_occupancy:
                return 0

        # "Otherwise, the seat's state does not change."
        return occupied

    def next_round(self):
        new_seats = {(x, y): self.next_seat_state(x, y) for x, y in self._seats}
        changed = self._seats != new_seats
        self._seats = new_seats
        return changed

    def run(self):
        while self.next_round():
            continue

        return sum(self._seats.values())


if __name__ == '__main__':
    for p in (1, 2):
        print(f"Problem {p}:")
        for filename in ("sample.txt", "input.txt"):
            print(Seats(filename, p).run())
