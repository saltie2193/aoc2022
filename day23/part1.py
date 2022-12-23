"""
Day 23: Unstable Diffusion
(https://adventofcode.com/2022/day/23)
"""

from __future__ import annotations

import functools
import os
from collections import defaultdict
from typing import Callable

import pytest
from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Elf = tuple[int, int]
Elves = set[Elf]
Movement = tuple[Callable[[Elf, Elves], bool], Callable[[Elf], Elf]]
move_map: dict[str, Elf] = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
    "NW": (-1, -1),
}


def print_elves(elves: Elves) -> None:
    max_x, max_y = tuple(map(max, zip(*elves)))
    min_x, min_y = tuple(map(min, zip(*elves)))
    print("".join("." for _ in range(min_y - 1, max_y + 2)))
    for i in range(min_x, max_x + 1):
        print(
            "".join(
                "#" if (i, j) in elves else "." for j in range(min_y - 1, max_y + 2)
            )
        )
    print("".join("." for _ in range(min_y - 1, max_y + 2)))
    print()


def targets_are_empty(elf: Elf, elves: Elves, targets: list[str]) -> bool:
    return not any(
        tuple(c + o for c, o in zip(elf, offset)) in elves
        for offset in map(move_map.get, targets)
    )


def move(elf: Elf, direction: str) -> Elf:
    offset = move_map.get(direction)
    return elf[0] + offset[0], elf[1] + offset[1]


check_move_n = functools.partial(targets_are_empty, targets=["N", "NE", "NW"])
check_move_s = functools.partial(targets_are_empty, targets=["S", "SE", "SW"])
check_move_w = functools.partial(targets_are_empty, targets=["W", "NW", "SW"])
check_move_e = functools.partial(targets_are_empty, targets=["E", "NE", "SE"])


def parse(input_str: str) -> set[Elf]:
    return set(
        (i, j)
        for i, line in enumerate(input_str.splitlines())
        for j, c in enumerate(line)
        if c == "#"
    )


def move_elf(elf: Elf, elves: Elves, movements: list[Movement]) -> Elf:
    for check, m in movements:
        if check(elf, elves):
            return m(elf)
    return elf


def move_elves(elves: Elves, movements: list[Movement]) -> Elves:
    proposals: defaultdict[Elf, list[Elf]] = defaultdict(list)
    for elf in elves:
        if targets_are_empty(elf, elves, ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]):
            proposals[elf] = [elf]
            continue

        proposals[move_elf(elf, elves, movements)].append(elf)

    res: set[Elf] = set()
    for new, old in proposals.items():
        if len(old) == 1:
            res.add(new)
            continue
        res.update(old)

    return res


def calc_empty_fields(elves: Elves) -> int:
    max_x, max_y = tuple(map(max, zip(*elves)))
    min_x, min_y = tuple(map(min, zip(*elves)))

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def compute(input_str: str) -> str:
    elves = parse(input_str)
    movements = [
        (check_move_n, functools.partial(move, direction="N")),
        (check_move_s, functools.partial(move, direction="S")),
        (check_move_w, functools.partial(move, direction="W")),
        (check_move_e, functools.partial(move, direction="E")),
    ]
    rounds = 10
    for r in range(rounds):
        elves = move_elves(elves, movements)
        movements.append(movements.pop(0))
    return str(calc_empty_fields(elves))


def test_check_moves() -> None:
    ins = [
        (check_move_n, {(-1, 0)}, False),
        (check_move_n, {(-1, 1)}, False),
        (check_move_n, {(-1, -1)}, False),
        (check_move_n, {((1, 0), (0, 1), (-1, 1), (-1, -1), (1, -1))}, True),
        (check_move_e, {(-1, 1)}, False),
        (check_move_e, {(0, 1)}, False),
        (check_move_e, {(-1, 1)}, False),
        (check_move_e, {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0)}, True),
        (check_move_s, {(1, -1)}, False),
        (check_move_s, {(1, 0)}, False),
        (check_move_s, {(1, 1)}, False),
        (check_move_s, {(-1, -1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1)}, True),
        (check_move_w, {(-1, -1)}, False),
        (check_move_w, {(0, -1)}, False),
        (check_move_w, {(1, -1)}, False),
        (check_move_w, {(-1, 0), (-1, 1), (0, 0), (0, 1), (1, 0), (1, 1)}, True),
    ]

    for fn, elves, res in ins:
        assert fn((0, 0), elves) == res


@pytest.mark.skip
def test_smaller() -> None:
    input_str = """\
.....
..##.
..#..
.....
..##.
.....
"""

    assert compute(input_str) == ""


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "110"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
