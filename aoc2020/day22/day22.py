from collections import deque


def read_decks(filename):
    with open(filename) as f:
        parts = f.read().split("\n\n")

    decks = [[int(line) for line in part.splitlines()[1:]] for part in parts]

    return decks


def get_score(deck):
    f = len(deck)
    return sum([card * (f - i) for i, card in enumerate(deck)])


def problem1(decks):
    deck1, deck2 = [deque(deck) for deck in decks]

    while deck1 and deck2:
        top1 = deck1.popleft()
        top2 = deck2.popleft()
        cards = sorted([top1, top2], reverse=True)
        if top1 > top2:
            deck1.extend(cards)
        else:
            deck2.extend(cards)

    winner = deck1 or deck2
    print(get_score(winner))


if __name__ == '__main__':
    problem1(read_decks("input.txt"))
