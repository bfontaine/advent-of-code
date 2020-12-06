from collections import Counter

def problem1():
    total = 0
    with open("input.txt") as f:
        for group in f.read().split("\n\n"):
            total += len(set(group.strip().replace("\n", "")))

    print(total)


def problem2():
    total = 0

    with open("input.txt") as f:
        for group in f.read().split("\n\n"):
            questions = Counter()
            people = group.strip().splitlines()
            size = len(people)
            for person in people:
                for question in person:
                    questions[question] += 1

            total += len([k for k, n in questions.items() if n == size])

    print(total)


if __name__ == '__main__':
    problem2()
