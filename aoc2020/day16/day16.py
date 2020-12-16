def parse_ticket(ticket_string):
    return [int(n) for n in ticket_string.split(",")]


def read_notes(filename):
    with open(filename) as f:
        sections = f.read().split("\n\n")

    classes = {}

    for line in sections[0].splitlines():
        name, specs = line.split(": ")
        classes[name] = []

        for spec in specs.split(" or "):
            a, b = spec.split("-")
            classes[name].append(range(int(a), int(b) + 1))

    _, ticket_string = sections[1].splitlines()

    ticket = parse_ticket(ticket_string)

    tickets = [parse_ticket(line) for line in sections[2].splitlines()[1:]]

    return classes, ticket, tickets


def valid_classes(classes, n):
    class_names = []
    for name, ranges in classes.items():
        for r in ranges:
            if n in r:
                class_names.append(name)
                break

    return class_names


def problem1(classes, _ticket, tickets):
    error_rate = 0

    for ticket in tickets:
        for n in ticket:
            if not valid_classes(classes, n):
                error_rate += n

    print(error_rate)


if __name__ == '__main__':
    problem1(*read_notes("input.txt"))
