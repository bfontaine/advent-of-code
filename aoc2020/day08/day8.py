def read_instructions(filename):
    instructions = []

    with open(filename) as f:
        for line in f:
            word, n = line.strip().split(" ")
            instructions.append((word, int(n)))

    return instructions

def run_program(instructions):
    acc = 0
    idx = 0
    seen_idx = set()
    end_idx = len(instructions)

    while True:
        if idx in seen_idx:
            return "infinite loop", acc

        if idx == end_idx:
            return "end", acc

        seen_idx.add(idx)

        instruction, n = instructions[idx]
        if instruction == "jmp":
            idx += n
            continue

        if instruction == "acc":
            acc += n
        idx += 1

    print(acc)


def problem1(filename):
    instructions = read_instructions(filename)
    _, acc = run_program(instructions)
    print(acc)

def problem2(filename):
    instructions = read_instructions(filename)
    for i, (word, n) in enumerate(instructions):
        if word == "acc":
            continue

        new_word = "jmp" if word == "nop" else "nop"
        test_instructions = instructions[:i] + [(new_word, n)] + instructions[i+1:]
        status, acc = run_program(test_instructions)
        if status == "end":
            print(acc)
            return


if __name__ == '__main__':
    problem2("input.txt")
