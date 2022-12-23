"""
Day 1: Calorie Counting - Part 1
https://adventofcode.com/2022/day/1
"""
from __future__ import annotations

import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Calories = int
Elf = list[Calories]


def parse(input_str: str) -> list[Elf]:
    return [[int(line) for line in elf.splitlines()] for elf in input_str.split("\n\n")]


def compute(input_str: str) -> str:
    return str(max(sum(elf) for elf in parse(input_str)))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "24000"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 1, 1

    aoc.run_part(year, day, part, compute, auto_submit=True)


if __name__ == "__main__":
    main()
