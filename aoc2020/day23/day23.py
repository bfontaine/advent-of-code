from collections import deque
from typing import Dict, List

import time


def read_cups(text):
    return tuple(int(n) for n in text)


def serialize_cups(cups):
    return "".join(str(cup) for cup in cups)


def serialize_cups_dict(cups_dict, start=1):
    cups: List[str] = []
    n = cups_dict[start]

    while n != start:
        cups.append(str(n))
        n = cups_dict[n]

    return "".join(cups)


SAMPLE = read_cups("389125467")
INPUT = read_cups("418976235")


def cups2dict(cups):
    # cup value -> next cup value
    d: Dict[int, int] = {}
    mx = len(cups) - 1
    for i, cup in enumerate(cups):
        if i == mx:
            d[cup] = cups[0]
            break

        d[cup] = cups[i + 1]

    return d


def move_dict(cups_dict, current):
    #     current -> next1 -> next2 -> next3 -> next4
    #                ^^^^^^^^^^^^^^^^^^^^^^^
    #                       remove
    #
    #     current ----------------------------> next4
    #
    #                       insert
    #                vvvvvvvvvvvvvvvvvvvvvvv
    # destination ----------------------------> destination_next
    # destination -> next1 -> next2 -> next3 -> destination_next
    next1 = cups_dict[current]
    next2 = cups_dict[next1]
    next3 = cups_dict[next2]
    next4 = cups_dict[next3]

    # remove next1/2/3
    cups_dict[current] = next4

    destination = current - 1
    while destination == next1 \
            or destination == next2 \
            or destination == next3 \
            or destination not in cups_dict:
        destination -= 1
        if destination < 1:
            d = next4
            m = next4
            while True:
                d = cups_dict[d]
                if d == current:
                    break
                if d > m:
                    m = d

            destination = m  # max(cups_dict)
            break

    destination_next = cups_dict[destination]
    cups_dict[destination] = next1
    cups_dict[next3] = destination_next


def move(cups: tuple):
    cups = deque(cups)

    current = cups.popleft()

    # 1- "The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from
    #     the circle; cup spacing is adjusted as necessary to maintain the circle."
    removed_cups = [cups.popleft() for _ in range(3)]
    remaining_cups = cups

    # 2- "The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
    #     If this would select one of the cups that was just picked up, the crab will keep subtracting one until
    #     it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest
    #     value on any cup's label, it wraps around to the highest value on any cup's label instead."
    lower_cup = None
    lower_i = None
    max_cup = None
    max_i = None
    for i, cup in enumerate(remaining_cups):
        if cup < current:
            # shortcut
            if cup + 1 == current:
                lower_i = i
                lower_cup = cup
                break

            if lower_cup is None:
                lower_i = i
                lower_cup = cup
            elif cup > lower_cup:
                lower_i = i
                lower_cup = cup

        if max_cup is None:
            max_i = i
            max_cup = cup
        elif cup > max_cup:
            max_i = i
            max_cup = cup

    if lower_cup is not None:
        destination_i = lower_i
    else:
        destination_i = max_i

    # 3- "The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
    #     They keep the same order as when they were picked up."
    destination_index = destination_i + 1

    # 4- "The crab selects a new current cup: the cup which is immediately clockwise of the current cup."
    # FIXME this is very inefficient
    new_cups = tuple(list(remaining_cups)[:destination_index]
                     + removed_cups
                     + list(remaining_cups)[destination_index:]
                     + [current])

    return new_cups


def problem1(cups):
    current = cups[0]
    cups_dict = cups2dict(cups)

    for _ in range(100):
        move_dict(cups_dict, current)
        current = cups_dict[current]

        # assert sorted(cups_dict.values()) == sorted(cups_dict)
        # print(serialize_cups_dict(cups_dict))

    print(serialize_cups_dict(cups_dict))


def problem2(cups):
    one_million = 1000000
    ten_million = 10 * one_million

    current = cups[0]
    # not really necessary to allocate a ~1M tuple here
    cups_dict = cups2dict(cups + tuple(range(max(cups) + 1, one_million + 1)))

    for n in range(ten_million):
        if n % one_million == 0:
            print(n)
        move_dict(cups_dict, current)
        current = cups_dict[current]

    next1 = cups_dict[1]
    next2 = cups_dict[next1]
    print(next1, next2, next1 * next2)


if __name__ == '__main__':
    problem2(INPUT)
