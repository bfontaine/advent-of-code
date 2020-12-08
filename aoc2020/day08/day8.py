def read_instructions(filename):
    instructions = []

    with open(filename) as f:
        for line in f:
            word, n = line.strip().split(" ")
            instructions.append((word, int(n)))

    return instructions

def problem1(filename):
    instructions = read_instructions(filename)
    acc = 0
    idx = 0
    seen_idx = set()

    while True:
        if idx in seen_idx:
            break

        seen_idx.add(idx)

        instruction, n = instructions[idx]
        if instruction == "jmp":
            idx += n
            continue

        if instruction == "acc":
            acc += n
        idx += 1

    print(acc)

if __name__ == '__main__':
    problem1("input.txt")