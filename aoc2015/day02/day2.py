def read_dimensions(filename):
    with open(filename) as f:
        for line in f:
            yield tuple(map(int, line.strip().split("x")))


def present_paper(dimensions):
    l, w, h = dimensions
    lw = l * w
    wh = w * h
    hl = h * l
    return 2 * lw + 2 * wh + 2 * hl + min(lw, wh, hl)


def present_ribbon(dimensions):
    l, w, h = dimensions
    n1, n2 = sorted(dimensions)[:2]
    return 2 * n1 + 2 * n2 + l * w * h


def run(dimensions):
    paper = 0
    ribbon = 0
    for present_dimensions in dimensions:
        paper += present_paper(present_dimensions)
        ribbon += present_ribbon(present_dimensions)

    print("paper:", paper, "ribbon:", ribbon)


if __name__ == '__main__':
    run(read_dimensions("input.txt"))
