# -*- coding: UTF-8 -*-

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

