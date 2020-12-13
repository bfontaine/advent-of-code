from functools import reduce


def read_notes(filename):
    with open(filename) as f:
        t, schedule = f.read().splitlines()
        return int(t), [None if bus == "x" else int(bus) for bus in schedule.split(",")]


def problem1(t, schedule):
    waiting_times = [((int(t / bus) + 1) * bus - t, bus) for bus in schedule if bus is not None]
    waiting_time, bus = min(waiting_times)
    print(bus, waiting_time, bus * waiting_time)


def problem2(schedule):
    # Refs:
    # "The Chinese Remainder Theorem made easy" https://www.youtube.com/watch?v=ru7mWZJlRQg
    # "The Chinese Remainder Theorem" https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
    #   See under "For Several Equations"
    #
    # Modular inverse exists in Python using pow(a, -1, p) but to understand:
    #   "Modular inverse made easy" https://www.youtube.com/watch?v=mgvA3z-vOzc
    #
    # [bus1   , bus2   , ..., busN]
    # [offset1, offset2, ..., offsetN]
    #
    # T = -offset1 [bus1]
    # T = -offset2 [bus2]
    # ...
    # T = -offsetN [busN]
    #
    #     ^^^^^^^^ = busI - offsetI = aI
    #
    # M = ∏ bus
    # bI = M/busI
    # bI' = bI^-1 [busI]
    #
    # T = ∑ aI * bI * bI'
    #
    schedule_with_offsets = [(bus, offset) for offset, bus in enumerate(schedule) if bus is not None]

    m = reduce(lambda a, b: a * b, [bus for bus, _ in schedule_with_offsets])
    t = 0
    for bus, offset in schedule_with_offsets:
        a = bus - offset
        b = m // bus
        c = pow(b, -1, bus)
        t += a * b * c

    print(t % m)


if __name__ == '__main__':
    notes = read_notes("input.txt")
    # problem1(*notes)
    _, s = notes
    problem2(s)
