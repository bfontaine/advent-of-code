import argparse


def run_game(starting_numbers, stop):
    last_turns = {}

    for i, n in enumerate(starting_numbers[:-1]):
        last_turns[n] = i + 1

    previous = starting_numbers[-1]

    for turn in range(len(starting_numbers) + 1, stop + 1):
        previous_turn = turn - 1

        if previous not in last_turns:
            last_turns[previous] = previous_turn
            previous = 0
            continue

        last_turn = last_turns[previous]
        last_turns[previous] = previous_turn

        previous = previous_turn - last_turn

    return previous


def main():
    p = argparse.ArgumentParser()
    p.add_argument("starting_numbers")
    starting_numbers = [int(n) for n in p.parse_args().starting_numbers.split(",")]

    print("Problem 1:", run_game(starting_numbers, 2020))
    print("Problem 2:", run_game(starting_numbers, 30000000))


if __name__ == '__main__':
    main()
