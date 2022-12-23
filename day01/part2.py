"""
Day 1: Calorie Counting - Part 2
https://adventofcode.com/2022/day/1#part2
"""
import os
import sys

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(HERE))
from part1 import parse

load_dotenv("../.venv")
API_TOKEN = os.getenv("API_TOKEN")


def compute(input_str: str) -> str:
    calories = map(sum, parse(input_str))
    return str(sum(sorted(calories, reverse=True)[0:3]))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()
    assert compute(input_s) == "45000"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 1, 2

    aoc.run_part(year, day, part, compute, auto_submit=True)


if __name__ == "__main__":
    main()
