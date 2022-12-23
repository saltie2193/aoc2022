"""
Day 4: Camp Cleanup - Part 2
https://adventofcode.com/2022/day/4#part2
"""
import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def compute(input_str: str) -> str:
    count = 0
    for line in input_str.splitlines():
        r0, r1 = [(int(a), int(b)) for a, b in [r.split("-") for r in line.split(",")]]
        if r0[0] <= r1[1] <= r0[1]:
            count += 1
        elif r1[0] <= r0[1] <= r1[1]:
            count += 1

    return str(count)


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()
    assert compute(input_s) == "4"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 4, 2

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
