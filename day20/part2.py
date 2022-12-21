from __future__ import annotations

import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def apply_rotation(_list: list, rotated: list[int]):
    if len(_list) != len(rotated):
        raise ValueError("Length of file and i_map do not match")

    return [_list[i] for i in rotated]


def print_rotated(_list: list, rotated: list[int]) -> None:
    print(rotated)
    print(apply_rotation(_list, rotated))


def rotate_update(index: int, value: int, rotation: list[int]) -> None:
    dist = value % (len(rotation) - 1)
    i = rotation.index(index)
    new_i = (i + dist) % (len(rotation) - 1)
    rotation.insert(new_i, rotation.pop(i))


def decrypt_file(file: list[int], key: int, rounds: int) -> list[int]:
    _file = [value * key for value in file]
    rotation = list(range(len(_file)))

    for _ in range(rounds):
        for i, _ in enumerate(rotation):
            value = _file[i]
            rotate_update(i, value, rotation)

    return apply_rotation(_file, rotation)


def compute(input_str: str) -> str:
    file = [int(line) for line in input_str.splitlines()]
    key = 811589153
    rounds = 10

    decrypted = decrypt_file(file, key, rounds)
    index = decrypted.index(0)
    coords = [
        decrypted[i % len(decrypted)] for i in range(index + 1000, index + 3001, 1000)
    ]
    return str(sum(coords))


def test_rotate_update() -> None:
    _list = [1, 2, -3, 3, -2, 0, 4]
    rotation = [i for i, _ in enumerate(_list)]
    rotations = [
        (2, [0, 1, 3, 4, 5, 2, 6]),
        (6, [0, 1, 2, 3, 6, 4, 5]),
        (1, [0, 2, 3, 1, 4, 5, 6]),
        (4, [0, 1, 4, 2, 3, 5, 6]),
        (5, rotation.copy()),
    ]

    for index, res in rotations:
        rot = rotation.copy()
        print(rot)
        rotate_update(index, _list[index], rot)
        print(rot)

        assert rot == res


def test_apply_rotation() -> None:
    _list = ["a", "b", "c", "d", "e", "f", "g"]
    rotations = [
        [0, 1, 2, 3, 4, 5, 6],
        [4, 0, 1, 2, 6, 5, 3],
    ]
    results = [_list.copy(), ["e", "a", "b", "c", "g", "f", "d"]]

    for rotation, result in zip(rotations, results):
        rotated = apply_rotation(_list, rotation)
        assert rotated == result


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "1623178306"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute, test=True)


if __name__ == "__main__":
    main()
