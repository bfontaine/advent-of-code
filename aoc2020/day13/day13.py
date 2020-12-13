def read_notes(filename):
    with open(filename) as f:
        t, schedule = f.read().splitlines()
        return int(t), [int(bus) for bus in schedule.split(",") if bus != "x"]


def problem1(t, schedule):
    waiting_times = [((int(t / bus) + 1) * bus - t, bus) for bus in schedule]
    waiting_time, bus = min(waiting_times)
    print(bus, waiting_time, bus * waiting_time)


if __name__ == '__main__':
    problem1(*read_notes("input.txt"))
