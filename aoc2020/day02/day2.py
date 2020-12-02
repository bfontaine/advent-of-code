#! /usr/bin/env python
# -*- coding: UTF-8 -*-

def parse_policy(policy):
    interval, char = policy.split(" ", 1)
    interval_parts = interval.split("-", 1)
    n1 = int(interval_parts[0])
    n2 = int(interval_parts[1])
    return n1, n2, char


def valid_password1(policy, password):
    mini, maxi, char = parse_policy(policy)

    return mini <= password.count(char) <= maxi

def valid_password2(policy, password):
    i, j, char = parse_policy(policy)

    return int(password[i-1] == char) + int(password[j-1] == char) == 1


def problem(policy_type=1):
    valid_fn = valid_password1 if policy_type == 1 else valid_password2

    with open("input.txt") as f:
        valid = 0

        for line in f:
            policy, password = line.strip().split(": ", 1)
            if valid_fn(policy, password):
                valid += 1

        print(valid)

if __name__ == "__main__":
    #problem(1)
    problem(2)
