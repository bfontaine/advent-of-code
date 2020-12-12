def run(filename):
    with open(filename) as f:
        instructions = f.read()

    n = 0
    first_basement_instruction = 0

    for i, instruction in enumerate(instructions):
        if instruction == "(":
            n += 1
        else:
            n -= 1
            if n == -1 and not first_basement_instruction:
                first_basement_instruction = i+1

    print("final floor:", n, "first basement:", first_basement_instruction)


if __name__ == '__main__':
    run("input.txt")
