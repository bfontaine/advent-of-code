class Instruction:
    MASK = 1
    ASSIGN = 2


MASK_SIZE = 36


def read_mask(mask):
    m = []

    for i in range(MASK_SIZE):
        bit = mask[MASK_SIZE - i - 1]
        m.append(None if bit == "X" else int(bit))

    return tuple(m)


def read_program(filename):
    instructions = []

    with open(filename) as f:
        for line in f:
            part1, part2 = line.strip().split(" = ")

            if line.startswith("mask"):
                instructions.append((Instruction.MASK, read_mask(part2)))
                continue

            address = int(part1[len("mem["):-1])
            value = int(part2)
            instructions.append((Instruction.ASSIGN, address, value))

    return instructions


def apply_mask(mask, value):
    # quite naive but it works

    bits_string = bin(value)[2:]  # remove '0b'
    bits = [int(b) for b in reversed(bits_string)] + [0] * (MASK_SIZE - len(bits_string))

    masked_bits = [m if m is not None else b for m, b in zip(mask, bits)]

    return int("".join(str(b) for b in reversed(masked_bits)), 2)


def problem1(instructions):
    mask = None
    memory = {}

    for instruction in instructions:
        code, *args = instruction

        if code == Instruction.MASK:
            mask = args[0]
            continue

        address, value = args
        memory[address] = apply_mask(mask, value)

    print(sum(memory.values()))


if __name__ == '__main__':
    program = read_program("input.txt")
    problem1(program)
