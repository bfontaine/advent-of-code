from typing import Tuple


def read_public_keys(filename) -> Tuple[int, int]:
    with open(filename) as f:
        l1, l2 = f
        return int(l1.strip()), int(l2.strip())


FACTOR = 20201227


def loop_size_from_public_key(public_key):
    subject_number = 7
    n = 1
    loop_size = 0
    while n != public_key:
        n = (n * subject_number) % FACTOR
        loop_size += 1

    return loop_size


def handshake1(subject_number, loop_size):
    n = 1
    for _ in range(loop_size):
        n = (n * subject_number) % FACTOR

    return n


def problem1(public_keys):
    pk1, pk2 = public_keys
    l1 = loop_size_from_public_key(pk1)
    l2 = loop_size_from_public_key(pk2)

    print(f"pk1={pk1}, pk2={pk2}, l1={l1}, l2={l2}")
    print(f"pk2_l1={handshake1(pk2, l1)}, pk1_l2={handshake1(pk1, l2)}")


if __name__ == '__main__':
    problem1(read_public_keys("input.txt"))
