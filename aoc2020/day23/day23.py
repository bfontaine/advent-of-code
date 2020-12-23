def read_cups(text):
    return [int(n) for n in text]


def serialize_cups(cups):
    return "".join(str(cup) for cup in cups)


SAMPLE = read_cups("389125467")
INPUT = read_cups("418976235")


def move(cups):
    current = cups[0]

    # 1- "The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from
    #     the circle; cup spacing is adjusted as necessary to maintain the circle."
    removed_cups = cups[1:4]
    remaining_cups = cups[4:]

    # 2- "The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
    #     If this would select one of the cups that was just picked up, the crab will keep subtracting one until
    #     it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest
    #     value on any cup's label, it wraps around to the highest value on any cup's label instead."
    lower_cups = sorted([cup for cup in remaining_cups if cup < current], reverse=True)
    if lower_cups:
        destination_cup = lower_cups[0]
    else:
        destination_cup = max(remaining_cups)

    # 3- "The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
    #     They keep the same order as when they were picked up."
    destination_index = remaining_cups.index(destination_cup) + 1

    # 4- "The crab selects a new current cup: the cup which is immediately clockwise of the current cup."
    cups = remaining_cups[:destination_index] + removed_cups + remaining_cups[destination_index:] + [current]
    return cups


def problem1(cups):
    for _ in range(100):
        # print(serialize_cups(cups))
        cups = move(cups)

    # print(serialize_cups(cups))

    start_index = cups.index(1)

    print(serialize_cups(cups[start_index + 1:] + cups[:start_index]))


if __name__ == '__main__':
    problem1(INPUT)
