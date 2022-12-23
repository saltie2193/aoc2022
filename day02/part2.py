"""
Day 2: Rock Paper Scissors - Part 2
https://adventofcode.com/2022/day/2#part2
"""
from __future__ import annotations

import os
import sys

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
from part1 import calc_player

load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

map_needed_token = {
    "AX": "C",
    "AY": "A",
    "AZ": "B",
    "BX": "A",
    "BY": "B",
    "BZ": "C",
    "CX": "B",
    "CY": "C",
    "CZ": "A",
}


def calc_round(a: str, b: str) -> tuple[int, int]:
    _b = map_needed_token[a + b]
    return calc_player(a, _b), calc_player(_b, a)


def compute(input_str: str) -> str:
    return str(
        sum(
            calc_round(a, b)[1]
            for a, b in [line.split() for line in input_str.splitlines()]
        )
    )


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "12"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 2, 2

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
