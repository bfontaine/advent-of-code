#! /usr/bin/env python
# -*- coding: UTF-8 -*-

def valid_password(policy, password):
    interval, char = policy.split(" ", 1)
    interval_parts = interval.split("-", 1)
    mini = int(interval_parts[0])
    maxi = int(interval_parts[1])

    return mini <= password.count(char) <= maxi


with open("input.txt") as f:
    valid = 0

    for line in f:
        policy, password = line.strip().split(": ", 1)
        if valid_password(policy, password):
            valid += 1

    print(valid)
