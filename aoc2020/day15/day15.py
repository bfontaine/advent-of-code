import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("starting_numbers")
    starting_numbers = p.parse_args().starting_numbers

    ls = [int(n) for n in starting_numbers.split(",")]

    while len(ls) < 2020:
        previous = ls[-1]

        try:
            seen_rindex = ls[-2::-1].index(previous)
        except ValueError:
            ls.append(0)
            continue

        prev_index = len(ls) - seen_rindex - 1
        ls.append(len(ls) - prev_index)

    print(ls[-1])


if __name__ == '__main__':
    main()
