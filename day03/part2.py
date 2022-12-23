"""
Day 3: Rucksack Reorganization - Part 2
https://adventofcode.com/2022/day/3#part2
"""
from __future__ import annotations

import os
import sys
from functools import reduce

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
from part1 import get_priority

load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def get_common_grp(rucksacks: list[str]) -> str:
    found = {}
    for rucksack, match_local in zip(rucksacks, [{} for _ in range(len(rucksacks))]):
        for item in rucksack:
            if item not in match_local:
                if item in found:
                    found[item] += 1
                else:
                    found[item] = 1

                match_local[item] = 1
                if found[item] >= 3:
                    return item


def compute(input_str: str) -> str:
    rucksacks = input_str.splitlines()

    def reducer(acc: list[list[str]], item: list[str]) -> list[list[str]]:
        if len(acc[-1]) >= 3:
            acc.append([item])
        else:
            acc[-1].append(item)
        return acc

    groups = reduce(reducer, rucksacks, [[]])
    # groups = reduce(lambda acc, r: acc.append(r) if len(acc[-1]) >= 3 else acc[-1].extend([r]),rucksacks,  [[]])
    prios = list(map(get_priority, map(get_common_grp, groups)))
    return str(sum(prios))


def test_get_common_grp() -> None:
    groups = [
        [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
        ],
        [
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw",
        ],
    ]

    expected = ["r", "Z"]

    for group, e in zip(groups, expected):
        assert get_common_grp(group) == e


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "70"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 3, 2

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
