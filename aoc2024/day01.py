from heapq import heapify, heappush, heappop

import aoc


def problem1(text: str):
    list1: list[int] = []
    list2: list[int] = []

    heapify(list1)
    heapify(list2)

    for line in text.splitlines():
        e1, e2 = line.split()
        heappush(list1, int(e1))
        heappush(list2, int(e2))

    n = 0

    while list1:
        smallest1 = heappop(list1)
        smallest2 = heappop(list2)
        n += abs(smallest1 - smallest2)

    return n


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
