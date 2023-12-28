from typing import List, Dict

import aoc


def hash_string(s: str):
    value = 0
    for c in s:
        ascii_code = ord(c)
        value += ascii_code
        value *= 17
        value %= 256

    return value


def parse_steps(text: str):
    return text.split(",")


def problem1(text: str):
    s = text.rstrip("\n")

    return sum(
        hash_string(step)
        for step in parse_steps(text)
    )


def problem2(text: str):
    boxes: List[Dict[str, int]] = [{} for _ in range(256)]

    for step in parse_steps(text):
        if "=" in step:
            label, focal_length_str = step.split("=", 1)
            focal_length = int(focal_length_str)
            box_index = hash_string(label)

            boxes[box_index][label] = focal_length
        else:
            assert step.endswith("-")
            label = step[:-1]
            box_index = hash_string(label)
            box = boxes[box_index]
            if label in box:
                del box[label]

    focusing_power = 0
    for box_index, box in enumerate(boxes):
        for lens_index, focal_length in enumerate(box.values()):
            lens_focusing_power = (box_index + 1) * (lens_index + 1) * focal_length
            focusing_power += lens_focusing_power

    return focusing_power


if __name__ == '__main__':
    aoc.run(problem1, problem2)
