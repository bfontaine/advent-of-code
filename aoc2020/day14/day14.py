class Instruction:
    MASK = 1
    ASSIGN = 2


MASK_SIZE = 36


def read_program(filename):
    instructions = []

    with open(filename) as f:
        for line in f:
            part1, part2 = line.strip().split(" = ")

            if line.startswith("mask"):
                instructions.append((Instruction.MASK, part2))
                continue

            address = int(part1[len("mem["):-1])
            value = int(part2)
            instructions.append((Instruction.ASSIGN, address, value))

    return instructions


def get_bits(value):
    bits_string = bin(value)[2:]  # remove '0b'
    return "0" * (MASK_SIZE - len(bits_string)) + bits_string


def apply_mask(mask, value):
    bits = get_bits(value)
    masked_bits = [m if m != "X" else b for m, b in zip(mask, bits)]
    return int("".join(masked_bits), 2)


def apply_floating_mask(mask, value):
    bits = get_bits(value)
    values = [""]

    for m, bit in zip(mask, bits):
        if m == "X":
            new_bits = "01"
        else:
            if m == "0":
                new_bits = bit
            else:
                new_bits = "1"

        new_values = []

        for b in new_bits:
            for value in values:
                new_values.append(value + b)

        values = new_values

    return [int(value, 2) for value in values]


def run(instructions, problem):
    mask = None
    memory = {}

    for instruction in instructions:
        code, *args = instruction

        if code == Instruction.MASK:
            mask = args[0]
            continue

        address, value = args

        if problem == 1:
            memory[address] = apply_mask(mask, value)
        else:
            for address in apply_floating_mask(mask, address):
                memory[address] = value

    print(sum(memory.values()))


if __name__ == '__main__':
    program = read_program("input.txt")
    run(program, problem=2)
