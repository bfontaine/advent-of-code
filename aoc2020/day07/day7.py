from collections import defaultdict

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

    start = "shiny gold"
    bags = {start, }
    size = len(bags)
    while True:
        for bag in list(bags):
            bags.update(containers[bag])

        new_size = len(bags)
        if new_size == size:
            break

        size = new_size

    bags.remove(start)
    print(len(bags), bags)


if __name__ == '__main__':
    problem1("input.txt")
