import aoc


def hash_string(s: str):
    value = 0
    for c in s:
        ascii_code = ord(c)
        value += ascii_code
        value *= 17
        value %= 256

    return value


def problem1(text: str):
    s = text.rstrip("\n")

    return sum(
        hash_string(step)
        for step in s.split(",")
    )


def problem2(text: str):
    raise NotImplementedError()


if __name__ == '__main__':
    aoc.run(problem1, problem2)
