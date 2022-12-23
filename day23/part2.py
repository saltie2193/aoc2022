"""
Day 23: Unstable Diffusion
(https://adventofcode.com/2022/day/23)
"""
from __future__ import annotations

import functools
import os
import sys

import pytest
from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(HERE))
from day23.part1 import (
    check_move_e,
    check_move_n,
    check_move_s,
    check_move_w,
    move,
    move_elves,
    parse,
)

load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def compute(input_str: str) -> str:
    elves = parse(input_str)
    movements = [
        (check_move_n, functools.partial(move, direction="N")),
        (check_move_s, functools.partial(move, direction="S")),
        (check_move_w, functools.partial(move, direction="W")),
        (check_move_e, functools.partial(move, direction="E")),
    ]
    r = 1
    prev = set()
    while prev != elves:
        prev = elves
        elves = move_elves(elves, movements)
        movements.append(movements.pop(0))
        if prev == elves:
            return str(r)
        r += 1

    return "0"


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

    assert compute(input_s) == "20"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
