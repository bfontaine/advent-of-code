from typing import Optional


def problem1():
    s = 0
    with open("input.txt") as f:
        for line in f:
            first_digit: Optional[str] = None
            last_digit: Optional[str] = None
            for c in line:
                if c.isnumeric():
                    if first_digit is None:
                        first_digit = c
                    last_digit = c

            n = int(first_digit + last_digit)
            s += n

    print(s)


if __name__ == '__main__':
    problem1()
