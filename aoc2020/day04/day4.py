import re

MANDATORY_FIELDS = {
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
    # "cid",  # (Country ID)
}


def parse_passport_fields(s):
    return re.findall(r"(?:^|\s)([a-z]+):", s)


def valid_password_fields(fields):
    return not (MANDATORY_FIELDS - set(fields))


def problem1():
    valid = 0

    with open("input.txt") as f:
        for raw_passport in f.read().split("\n\n"):
            fields = parse_passport_fields(raw_passport)
            if valid_password_fields(fields):
                valid += 1

    print(valid)


if __name__ == '__main__':
    problem1()
