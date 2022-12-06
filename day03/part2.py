import os
from functools import reduce
from typing import List

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def get_common_grp(rucksacks: List[str]) -> str:
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


def get_priority(c: str) -> int:
    value = ord(c)
    if value >= 97:
        return value - 96
    if value >= 65:
        return value - 38


def compute(input_str: str) -> str:
    rucksacks = input_str.splitlines()

    def reducer(acc: List[List[str]], item: List[str]) -> List[List[str]]:
        if len(acc[-1]) >= 3:
            acc.append([item])
        else:
            acc[-1].append(item)
        return acc

    groups = reduce(reducer, rucksacks, [[]])
    # groups = reduce(lambda acc, r: acc.append(r) if len(acc[-1]) >= 3 else acc[-1].extend([r]),rucksacks,  [[]])
    badges = [get_common_grp(group) for group in groups]
    prios = list(map(get_priority, badges))
    return sum(prios)


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
    input_s = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
    assert compute(input_s) == 70


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 3, 2

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
