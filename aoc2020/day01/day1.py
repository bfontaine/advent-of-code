# -*- coding: UTF-8 -*-

def problem1():
    seen = set()

    with open("input.txt") as f:
        for line in f:
            n = int(line.strip())
            m = 2020 - n
            if m not in seen:
                seen.add(n)
                continue

            print(n * m)
            break

def problem2():
    numbers = []

    with open("input.txt") as f:
        for line in f:
            numbers.append(int(line.strip()))

    numbers.sort()

    seen2 = {}

    for n1 in numbers:
        difference = 2020 - n1
        for n2 in numbers:
            if n2 <= n1:
                continue
            if n2 > difference:
                break

            seen2[n1 + n2] = n1*n2

    for n in numbers:
        m = 2020 - n
        if m in seen2:
            print(seen2[m] * n)
            return


if __name__ == "__main__":
    #problem1()
    problem2()
