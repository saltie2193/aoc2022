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
    SOLID = "#"
    FALLING = "@"


input_rocks = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


def chamber_to_str(
    solid: set[tuple[int, int]], falling: list[list[tuple[int, int]]], width: int
) -> str:
    lines: list[list[str]] = []
    falling_set = {field for rock in falling for field in rock}
    max_row = max(*(r for r, _ in solid), *(r for r, _ in falling_set))

    for row in range(max_row + 1):
        line = ["|"]
        for col in range(0, width):
            if (row, col) in solid:
                line.append("#")
            elif (row, col) in falling_set:
                line.append("@")
            else:
                line.append(".")
        line.append("|")
        lines.append(line)

    lines = [["_" for _ in range(0, width + 2)], *lines]

    return "\n".join("".join(line) for line in lines)


def make_solid(
    solid: set[tuple[int, int]],
    rock: list[tuple[int, int]],
    col_floor: list[int],
) -> tuple[set[tuple[int, int]], list[int]]:
    for field in rock:
        if field in solid:
            print(f"ups? {field}")
        col_floor[field[1]] = field[0]
        solid.add(field)
    return solid, col_floor


def simulate_chamber(
    action: str,
    solid: set[tuple[int, int]],
    falling: list[list[tuple[int, int]]],
    col_floor: list[int],
    width: int = 7,
) -> tuple[set[tuple[int, int]], list[list[tuple[int, int]]], list[int]]:
    # print(chamber_to_str(solid, falling, 7))
    # print()

    rock = falling[0]
    if action == ">":
        offset = 1
    elif action == "<":
        offset = -1
    else:
        raise ValueError(f"Unknown direction {action}")

    moved = []
    for row, col in rock:
        new_col = col + offset
        if new_col >= width or col + new_col < 0 or (row, new_col) in solid:
            moved = rock
            break
        moved.append((row, new_col))

    # move down
    fallen = []
    for row, col in moved:
        row_below = row - 1
        if (row_below, col) in solid or row_below < 0:
            solid, col_floor = make_solid(solid, moved, col_floor)
            return solid, falling[1:], col_floor

        fallen.append((row_below, col))
    falling[0] = fallen

    return solid, falling, col_floor


def spawn_rock(
    solid: set[tuple[int, int]], shape: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    offset_col = 2
    offset_row = 3

    if len(solid) > 0:
        offset_row = max(r for r, _ in solid) + 4

    return [(row + offset_row, col + offset_col) for row, col in shape]


def compute(input_str: str) -> str:
    import cProfile

    with cProfile.Profile() as pr:
        shapes = [
            [(0, 0), (0, 1), (0, 2), (0, 3)],  # line
            [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # cross
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],  # L
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # square
        ]

        shapes_index = 0
        actions = input_str.strip()
        solid = set()
        falling = []
        i = 0
        width = 7
        col_floor = [-1 for _ in range(width)]
        target = 1_000_000_000_000

        while shapes_index < target + 1:
            if len(falling) < 1:
                if shapes_index % 10_000 == 0:
                    print(f"{shapes_index}/{target} ({shapes_index/target:.2%})")
                    pass
                rock = spawn_rock(solid, shapes[shapes_index % len(shapes)])
                falling.append(rock)
                shapes_index += 1

            solid, falling, col_floor = simulate_chamber(
                actions[i % len(actions)], solid, falling, col_floor, width
            )
            min_floor = max(col_floor)
            solid = {f for f in solid if f[0] > min_floor - 50}

            i += 1

        pr.print_stats()
        return str(max(r for r, _ in solid) + 1)


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()
    assert compute(input_s) == "3068"


def test_spawn_rock_simple() -> None:
    shapes = [
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # line
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # cross
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],  # L
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # square
    ]
    rocks = [
        [(3, 2), (3, 3), (3, 4), (3, 5)],
        [(3, 3), (4, 2), (4, 3), (4, 4), (5, 3)],
        [(3, 2), (3, 3), (3, 4), (4, 4), (5, 4)],
        [(3, 2), (4, 2), (5, 2), (6, 2)],
        [(3, 2), (3, 3), (4, 2), (4, 3)],
    ]
    for shape, rock in zip(shapes, rocks):
        assert spawn_rock(set(), shape) == rock


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
