from collections import defaultdict


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


def valid_class(ranges, n):
    for r in ranges:
        if n in r:
            return True

    return False


def valid_classes(classes, n):
    class_names = []
    for name, ranges in classes.items():
        if valid_class(ranges, n):
            class_names.append(name)

    return class_names


def problem1(classes, _ticket, tickets):
    error_rate = 0

    for ticket in tickets:
        for n in ticket:
            if not valid_classes(classes, n):
                error_rate += n

    print(error_rate)


def valid_ticket(classes, ticket):
    for n in ticket:
        if not valid_classes(classes, n):
            return False
    return True


def problem2(classes, ticket, tickets):
    valid = defaultdict(set)
    invalid = defaultdict(set)

    for tk in tickets:
        if not valid_ticket(classes, tk):
            continue

        for i, n in enumerate(tk):
            for name, ranges in classes.items():
                if valid_class(ranges, n):
                    valid[i].add(name)
                else:
                    invalid[i].add(name)

    known_classes = {}
    classes_count = len(classes)

    while len(known_classes) != classes_count:
        for i in list(valid):
            names = (valid[i] - invalid[i] - set(known_classes))
            if len(names) == 1:
                name = list(names)[0]
                known_classes[name] = i
                del valid[i]

    p = 1

    for name, i in known_classes.items():
        if name.startswith("departure"):
            p *= ticket[i]

    print(p)


if __name__ == '__main__':
    problem2(*read_notes("input.txt"))
