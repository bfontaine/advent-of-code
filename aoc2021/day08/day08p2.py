# -*- coding: UTF-8 -*-

import sys
from collections import defaultdict

def read_digits(s):
    return [set(d) for d in s.strip().split(" ")]

def serialize_digit(s):
    return "".join(sorted(s))

def take_one(s):
    e = s.pop()
    assert not s
    return e


def main():
    total = 0

    for line in sys.stdin:
        digits_string, display_string = line.split("|")
        digits = read_digits(digits_string)
        display = read_digits(display_string)

        by_size = defaultdict(list)
        for digit in digits:
            by_size[len(digit)].append(digit)

        known_digits = [None]*10

        _1 = by_size[2][0]
        _7 = by_size[3][0]
        _4 = by_size[4][0]
        _8 = by_size[7][0]
        _235 = by_size[5]
        _069 = by_size[6]

        top = take_one(_7 - _1)

        for digit in _069:
            if s := _1 - digit:
                top_right = take_one(s)
                _6 = digit
                _069.remove(digit)
                _09 = _069
                break

        for digit in _09:
            s = digit - _7 - _4
            if len(s) == 1:
                _9 = digit
                _09.remove(_9)
                _0 = take_one(_09)
                assert not _09
                bottom = take_one(s)
                break

        bottom_right = take_one(_1 - {top_right,})

        so_far = {top, top_right, bottom_right, bottom}

        for digit in _235:
            s = digit - so_far
            if len(s) == 1:
                middle = take_one(s)
                so_far.add(middle)
                _3 = digit
                _235.remove(_3)
                _25 = _235
                break

        top_left = take_one(_4 - so_far)
        so_far.add(top_left)

        bottom_left = take_one(set("abcdefg") - so_far)

        mapping = {
                serialize_digit(d): n
                for d, n in (
                    (_0, 0),
                    (_1, 1),
                    (top + top_right + middle + bottom_left + bottom, 2),
                    (_3, 3),
                    (_4, 4),
                    (top + top_left + middle + bottom_right + bottom, 5),
                    (_6, 6),
                    (_7, 7),
                    (_8, 8),
                    (_9, 9),
                )
        }

        number = 0

        for digit in display:
            n = mapping[serialize_digit(digit)]
            number = number * 10 + n

        total += number

    print(total)


if __name__ == "__main__":
    main()
