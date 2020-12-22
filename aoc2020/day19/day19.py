import re


def parse_rules(text: str):
    rules = {}

    for line in text.splitlines():
        node, deps_string = line.split(": ")
        alternative_texts = deps_string.split(" | ")
        alternatives = [[s[1:-1] if s[0] == '"' else int(s) for s in alt.split()] for alt in alternative_texts]

        rules[int(node)] = alternatives

    return rules


def read_file(filename):
    with open(filename) as f:
        rules, messages = f.read().split("\n\n")

    return parse_rules(rules), messages.strip().splitlines()


def resolve_rule(rules, node, problem):
    if problem == 2:
        if node == 8:
            # '8: 42 | 42 8' == one or more of 42
            return resolve_rule(rules, 42, 2) + "+"

        if node == 11:
            # '11: 42 31 | 42 11 31' = aa...abb...b where count(a) == count(b)
            before = resolve_rule(rules, 42, 2)
            after = resolve_rule(rules, 31, 2)

            resolved_alternatives = []

            # quick and dirty, but it works (longest message = 96 (2*48) chars)
            for n in range(1, 49):
                resolved_alternatives.append(before * n + after * n)

            return "(?:%s)" % "|".join(resolved_alternatives)

    alternatives = rules[node]
    resolved_alternatives = []
    for alternative in alternatives:
        resolved_alternative = ""

        for n in alternative:
            resolved_alternative += n if isinstance(n, str) else resolve_rule(rules, n, problem)

        resolved_alternatives.append(resolved_alternative)

    if len(resolved_alternatives) == 1:
        return resolved_alternatives[0]

    if all([len(alt) == 1 for alt in resolved_alternatives]):
        return "[%s]" % "".join(resolved_alternatives)

    return "(?:%s)" % "|".join(resolved_alternatives)


def run(problem, rules, messages):
    rule = re.compile("^%s$" % resolve_rule(rules, 0, problem))

    n = 0
    for message in messages:
        if rule.match(message):
            n += 1

    print(n)


if __name__ == '__main__':
    run(2, *read_file("input.txt"))
