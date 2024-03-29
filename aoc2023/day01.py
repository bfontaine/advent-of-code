import re

import aoc

DIGITS = {
    s: i + 1
    for i, s in enumerate([
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    ])
}

DIGITS_RE = re.compile(r"\d|" + "|".join(DIGITS))
DIGITS_REV_RE = re.compile(r"\d|" + "|".join("".join(reversed(d)) for d in DIGITS))


def get_digit_value(s: str) -> int:
    if len(s) == 1:
        return int(s)

    return DIGITS[s]


def get_line_calibration_value(line: str, p: int):
    if p == 1:
        digits = [c for c in line if c.isdigit()]
    else:
        digit1 = next(DIGITS_RE.finditer(line))
        digit2 = next(DIGITS_REV_RE.finditer("".join(reversed(line))))
        digits = [
            digit1.group(0),
            "".join(reversed(digit2.group(0))),
        ]

    first_n = get_digit_value(digits[0])
    last_n = get_digit_value(digits[-1])

    return first_n * 10 + last_n


def problem(p: int, text: str):
    s = 0
    for line in text.splitlines():
        n = get_line_calibration_value(line, p=p)
        s += n

    return s


def problem1(text: str): return problem(1, text)


def problem2(text: str): return problem(2, text)


if __name__ == '__main__':
    aoc.run(problem1, problem2)
