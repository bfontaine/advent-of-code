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


def resolve_rule(rules, node):
    alternatives = rules[node]
    resolved_alternatives = []
    for alternative in alternatives:
        resolved_alternative = ""

        for n in alternative:
            resolved_alternative += n if isinstance(n, str) else resolve_rule(rules, n)

        resolved_alternatives.append(resolved_alternative)

    if len(resolved_alternatives) == 1:
        return resolved_alternatives[0]

    if all([len(alt) == 1 for alt in resolved_alternatives]):
        return "[%s]" % "".join(resolved_alternatives)

    return "(?:%s)" % "|".join(resolved_alternatives)


def problem1(rules, messages):
    rule = re.compile("^%s$" % resolve_rule(rules, 0))

    n = 0
    for message in messages:
        if rule.match(message):
            n += 1

    print(n)


if __name__ == '__main__':
    problem1(*read_file("input.txt"))
