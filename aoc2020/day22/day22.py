from collections import deque


def read_decks(filename):
    with open(filename) as f:
        parts = f.read().split("\n\n")

    decks = [deque([int(line) for line in part.splitlines()[1:]]) for part in parts]

    return decks


def get_score(deck):
    f = len(deck)
    return sum([card * (f - i) for i, card in enumerate(deck)])


def problem1(deck1, deck2):
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


def recursive_combat(decks, game=1):
    seen = set()
    game_round = 0

    while all(decks):
        game_round += 1

        # "Before either player deals a card, if there was a previous round in this game that had exactly the same cards
        #  in the same order in the same players' decks, the game instantly ends in a win for player 1."
        situation = tuple(tuple(deck) for deck in decks)
        if situation in seen:
            return 0

        seen.add(situation)

        """
        print(f"== Round {game_round} (Game {game}) ==")
        for i, deck in enumerate(decks):
            print(f"Player {i + 1}'s deck:", ", ".join(str(card) for card in decks[i]))
        print()
        # """

        # "Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing
        #  the top card of their deck as normal."
        tops = [deck.popleft() for deck in decks]

        # "If both players have at least as many cards remaining in their deck as the value of the card they just drew,
        #  the winner of the round is determined by playing a new game of Recursive Combat"
        if all(len(deck) >= top for deck, top in zip(decks, tops)):
            deck_copies = [deque(list(deck)[:top]) for top, deck in zip(tops, decks)]
            winner = recursive_combat(deck_copies, game + 1)
            cards = [tops[winner], tops[(winner + 1) % 2]]
        else:
            # normal game
            cards = sorted(tops, reverse=True)
            winner = tops.index(cards[0])

        decks[winner].extend(cards)

    if decks[0]:
        return 0
    return 1


def problem2(*decks):
    winner = recursive_combat(decks)
    winner_deck = decks[winner]
    print(get_score(winner_deck))


if __name__ == '__main__':
    # 36417 = too high
    problem2(*read_decks("input.txt"))
