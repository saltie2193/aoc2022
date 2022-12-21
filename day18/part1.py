from __future__ import annotations

import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def parse(input_str: str) -> set[tuple[int, int, int]]:
    return {tuple(map(int, line.split(","))) for line in input_str.splitlines()}


def get_empty_neighbors(
    cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]
) -> list[tuple[int, int, int]]:
    x, y, z = cube

    neighbors = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    return [neighbor for neighbor in neighbors if neighbor not in cubes]


def count_free_surfaces(
    cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]
) -> int:
    return len(get_empty_neighbors(cube, cubes))


def compute(input_str: str) -> str:
    cubes = set(parse(input_str))
    count_sum = 0
    for cube in cubes:
        free_surfaces = count_free_surfaces(cube, cubes)
        count_sum += free_surfaces

    return str(count_sum)


def test() -> None:
    input_s = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
    assert compute(input_s) == "64"


def test_simple() -> None:
    input_s = """\
1,1,1
2,1,1
"""
    assert compute(input_s) == "10"


def test_parse() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    out = {
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5),
    }

    assert parse(input_s) == out


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
