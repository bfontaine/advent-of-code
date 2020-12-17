class Base17:
    def __init__(self, filename):
        self.state = set()

        with open(filename) as f:
            for y, line in enumerate(f):
                for x, c in enumerate(line.strip()):
                    if c == "#":
                        self.set_initial_state(x, y)

    def set_initial_state(self, x, y):
        raise NotImplementedError()

    def get_neighbors(self, coords):
        raise NotImplementedError()

    def next_state(self):
        seen = set()
        new_state = set()

        for coords in self.state:
            if coords in seen:
                continue

            neighbors = self.get_neighbors(coords)

            # active cells
            if len([cx for cx in neighbors if cx in self.state]) in {2, 3}:
                new_state.add(coords)

            seen.add(coords)

            for cx in neighbors:
                if cx in seen:
                    continue

                if cx in self.state:
                    continue

                # inactive cells
                if len([cx_ for cx_ in self.get_neighbors(cx) if cx_ in self.state]) == 3:
                    new_state.add(cx)

                seen.add(cx)

        self.state = new_state

    def run(self):
        for _ in range(6):
            self.next_state()

        print(len(self.state))


class Problem1(Base17):
    def set_initial_state(self, x, y):
        self.state.add((x, y, 0))

    def get_neighbors(self, coords):
        x, y, z = coords
        return [(x1, y1, z1)
                for x1 in (x - 1, x, x + 1)
                for y1 in (y - 1, y, y + 1)
                for z1 in (z - 1, z, z + 1)
                if (x1, y1, z1) != (x, y, z)]


class Problem2(Base17):
    def set_initial_state(self, x, y):
        self.state.add((x, y, 0, 0))

    def get_neighbors(self, coords):
        x, y, z, w = coords
        return [(x1, y1, z1, w1)
                for x1 in (x - 1, x, x + 1)
                for y1 in (y - 1, y, y + 1)
                for z1 in (z - 1, z, z + 1)
                for w1 in (w - 1, w, w + 1)
                if (x1, y1, z1, w1) != (x, y, z, w)]


if __name__ == '__main__':
    # Problem1("input.txt").run()
    Problem2("input.txt").run()
