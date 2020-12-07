from collections import defaultdict, Counter

START = "shiny gold"

def read_rules(filename):
    # color -> color -> number
    bags = {}

    with open(filename) as f:
        # "light red bags contain 1 bright white bag, 2 muted yellow bags."
        # "bright white bags contain 1 shiny gold bag."
        # "faded blue bags contain no other bags."
        for line in f:
            # look ma, no regex
            parent_bag_color, content = line.strip().split(" bags contain ")
            bags[parent_bag_color] = {}

            if content == "no other bags.":
                continue

            for fragment in content.split(", "):
                # 1 bright white bag
                n, color1, color2, _ = fragment.split(" ")
                color = " ".join((color1, color2))
                bags[parent_bag_color][color] = int(n)

    return bags


def problem1(filename):
    rules = read_rules(filename)

    # child_bag -> parent_bag
    containers = defaultdict(set)
    for parent_bag, child_bags in rules.items():
        for child_bag in child_bags:
            containers[child_bag].add(parent_bag)

    bags = {START, }
    size = len(bags)
    while True:
        for bag in list(bags):
            bags.update(containers[bag])

        new_size = len(bags)
        if new_size == size:
            break

        size = new_size

    bags.remove(START)
    print(len(bags), bags)


def problem2(filename):
    rules = read_rules(filename)
    # bag -> # of occurrences

    total = 0

    leaves = Counter()
    leaves[START] = 1

    while True:
        new_leaves = Counter()

        for bag, count in leaves.items():
            new_leaves.update({child_bag: n*count for child_bag, n in rules[bag].items()})

        if not new_leaves:
            break

        total += sum(new_leaves.values())
        leaves = new_leaves

    print(total)


if __name__ == '__main__':
    problem2("input.txt")
