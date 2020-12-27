from typing import Dict, List

import itertools


def read_cups(text):
    return [int(n) for n in text]


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

    first = None
    prev = None
    current = None
    for cup in cups:
        if first is None:
            first = cup
            prev = cup
            continue

        current = cup
        d[prev] = cup
        prev = current

    d[current] = first

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
    cups_dict = cups2dict(itertools.chain(cups, range(max(cups) + 1, one_million + 1)))

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
