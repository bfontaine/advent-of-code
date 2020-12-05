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
    return dict(re.findall(r"(?:^|\s)([a-z]+):(\S+)", s))


def valid_range(field_value, mini, maxi):
    return field_value.isdigit() and mini <= int(field_value) <= maxi


def valid_password_fields(fields, problem):
    field_names = set(fields)
    all_mandatory_are_present = not (MANDATORY_FIELDS - set(field_names))

    if not all_mandatory_are_present:
        return False

    if problem == 1:
        return True

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not valid_range(fields["byr"], 1920, 2002) \
            or not valid_range(fields["iyr"], 2010, 2020) \
            or not valid_range(fields["eyr"], 2020, 2030):
        return False

    # hgt (Height) - a number followed by either cm or in:
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    height = fields["hgt"]
    height_unit = height[-2:]
    height_value = height[:-2]

    if height_unit == "cm":
        if not valid_range(height_value, 150, 193):
            return False
    elif height_unit == "in":
        if not valid_range(height_value, 59, 76):
            return False
    else:
        return False

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not re.match(r"#[0-9a-f]{6}$", fields["hcl"]):
        return False

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if fields["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.match(r"\d{9}$", fields["pid"]):
        return False

    return True


def run_problem(problem):
    valid = 0

    with open("input.txt") as f:
        content = f.read()

        for raw_passport in content.split("\n\n"):
            fields = parse_passport_fields(raw_passport)
            if valid_password_fields(fields, problem):
                valid += 1

    print(valid)


def problem1():
    run_problem(1)


def problem2():
    run_problem(2)


if __name__ == '__main__':
    problem2()
