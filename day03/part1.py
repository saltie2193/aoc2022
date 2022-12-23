"""
Day 3: Rucksack Reorganization - Part 1
https://adventofcode.com/2022/day/3
"""
import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def get_common(input_str: str) -> str:
    half = len(input_str) // 2
    a, b = input_str[:half], input_str[half:]
    in_a = {}
    in_b = {}
    for _a, _b in zip(a, b):
        if _a == _b:
            return _a
        if _b in in_a:
            return _b
        if _a in in_b:
            return _a

        in_a[_a] = True
        in_b[_b] = True


def get_priority(c: str) -> int:
    value = ord(c)
    if value >= 97:
        return value - 96
    if value >= 65:
        return value - 38


def compute(input_str: str) -> str:
    commons = map(get_common, input_str.splitlines())
    return str(sum(map(get_priority, commons)))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "157"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 3, 1

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
