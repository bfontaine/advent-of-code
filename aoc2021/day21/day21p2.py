import sys
import itertools
from collections import Counter
from functools import cache

DICE_VALUES = (1, 2, 3)
ROLLS = 3
PLAYERS = (1, 2)


def get_dice_sums():
    sums = Counter()

    for dices in itertools.product(DICE_VALUES, repeat=ROLLS):
        sums[sum(dices)] += 1

    return tuple(dict(sums).items())


DICE_SUMS = get_dice_sums()

# cuts the time from 30s to 3s
@cache
def next_turn(position1, position2, score1, score2, multiplier=1):
    wins1 = 0
    wins2 = 0
    for sum1, multiplier1 in DICE_SUMS:
        next_position1 = position1 + sum1
        if next_position1 > 10:
            next_position1 -= 10

        next_score1 = score1 + next_position1

        for sum2, multiplier2 in DICE_SUMS:
            multiplier_ = multiplier * multiplier1 * multiplier2

            if next_score1 >= 21:
                wins1 += multiplier_
                break

            next_position2 = position2 + sum2
            if next_position2 > 10:
                next_position2 -= 10

            next_score2 = score2 + next_position2
            if next_score2 >= 21:
                wins2 += multiplier_
                continue

            wins1_, wins2_ = next_turn(next_position1, next_position2, next_score1, next_score2, multiplier_)
            wins1 += wins1_
            wins2 += wins2_

    return wins1, wins2


def main():
    positions = {}
    # Player 1 starting position: 4
    # Player 2 starting position: 8
    for line in sys.stdin:
        _, player, _, _, position = line.split(" ")
        positions[int(player)] = int(position)

    win1, win2 = next_turn(positions[1], positions[2], 0, 0)
    print(win1, win2)
    print(max(win1, win2))


if __name__ == '__main__':
    main()
