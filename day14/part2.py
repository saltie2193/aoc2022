from __future__ import annotations

import os
from enum import Enum

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


class Terrain(Enum):
    AIR = "."
    ROCK = "#"
    SAND = "o"
    ORIGIN = "+"


def terrain_to_str(terrain: list[list[Terrain]], floor: int) -> str:
    lines = []
    left = len(terrain[0])
    for row in terrain:
        line = ""
        l, r = None, None
        for i, cell in enumerate(row):
            line += cell.value
            if cell is not Terrain.AIR and l is None:
                l = i
        if l is not None and l < left:
            left = l
        lines.append(line)
    while len(lines) < floor + 1:
        lines.append("".join([str(Terrain.AIR.value) for _ in enumerate(terrain[0])]))
    lines[floor] = "".join([str(Terrain.ROCK.value) for _ in enumerate(terrain[0])])
    return "\n".join(line[left:] for line in lines)


def parse_vector(input_str: str) -> list[tuple[int, int]]:
    vector = []
    for cord in input_str.split(" -> "):
        i, j = cord.split(",")
        vector.append((int(i), int(j)))

    return vector


def set_terrain(
    terrain: list[list[Terrain]], col: int, row: int, kind: Terrain, default=Terrain.AIR
) -> list[list[Terrain]]:
    for row_i, _ in enumerate(terrain):
        while len(terrain[row_i]) <= col:
            terrain[row_i].append(default)

    while len(terrain) <= row:
        terrain.append([default for _ in range(col + 1)])

    terrain[row][col] = kind

    return terrain


def gen_terrain(vectors: list[list[tuple[int, int]]]) -> list[list[Terrain]]:
    terrain = []

    for vector in vectors:
        if len(vector) == 1:
            terrain = set_terrain(terrain, *vector[0], Terrain.ROCK)

        i = 0
        while i + 1 < len(vector):
            a, b = sorted(vector[i : i + 2])

            if a[0] == b[0]:
                low, high = a[1], b[1]
                p = [(a[0], _j) for _j in range(low, high + 1)]
            else:
                low, high = a[0], b[0]
                p = [(_i, a[1]) for _i in range(low, high + 1)]

            for cord in p:
                terrain = set_terrain(terrain, *cord, Terrain.ROCK)
            # print(terrain_to_str(terrain))
            i += 1

    return terrain


def parse(input_str) -> tuple[list[list[Terrain]], int]:
    vectors = list(map(parse_vector, input_str.splitlines()))
    floor = max(max(r for _, r in vector) for vector in vectors) + 2
    terrain = gen_terrain(vectors)
    terrain = set_terrain(terrain, 500, 0, Terrain.ORIGIN)

    return terrain, floor


def simulate_sand(
    terrain: list[list[Terrain]], sand: list[tuple[int, int]], floor: int
) -> tuple[list[list[Terrain]], list[tuple[int, int]]]:

    moving_sand: list[tuple[int, int]] = []
    for col, row in sorted(
        sorted(sand, key=lambda a: a[0]), key=lambda a: a[1], reverse=True
    ):
        row_below = row + 1
        for row_i, _ in enumerate(terrain):
            while len(terrain[row_i]) <= col + 1:
                terrain[row_i].append(Terrain.AIR)

        while len(terrain) <= row_below:
            terrain.append([Terrain.AIR for _ in range(col + 2)])

        # floor
        if row_below >= floor:
            terrain[row][col] = Terrain.SAND
            continue

        # below
        if terrain[row_below][col] == Terrain.AIR:
            terrain[row][col] = Terrain.AIR
            terrain[row_below][col] = Terrain.SAND
            moving_sand.append((col, row_below))
            continue

        # below left
        if terrain[row_below][col - 1] == Terrain.AIR:
            terrain[row][col] = Terrain.AIR
            terrain[row_below][col - 1] = Terrain.SAND
            moving_sand.append((col - 1, row_below))
            continue

        # below right
        if terrain[row_below][col + 1] == Terrain.AIR:
            terrain[row][col] = Terrain.AIR
            terrain[row_below][col + 1] = Terrain.SAND
            moving_sand.append((col + 1, row_below))
            continue

        terrain[row][col] = Terrain.SAND

    return terrain, moving_sand


def compute(input_str: str) -> str:
    terrain, floor = parse(input_str)
    print(floor)
    print(terrain_to_str(terrain, floor))

    sand = []
    i = 0
    while i < 50000:
        sand.append((500, 0))
        i += 1

        terrain, sand = simulate_sand(terrain, sand, floor)
        # print(terrain_to_str(terrain))

        print(len(sand))
        if len(sand) <= 0:
            break
    print(terrain_to_str(terrain, floor))
    return str(i - len(sand))


def test_parse_vector() -> None:
    inputs = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]
    exp = [[(498, 4), (498, 6), (496, 6)], [(503, 4), (502, 4), (502, 9), (494, 9)]]

    for i, e in zip(inputs, exp):
        assert parse_vector(i) == e


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "93"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
