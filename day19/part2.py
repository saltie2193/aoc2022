from __future__ import annotations

import os
from functools import reduce

from aoc import AOC
from dotenv import load_dotenv
from tqdm import tqdm

from day19.part1 import get_max_geodes, parse

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def compute(input_str: str) -> str:
    factories = parse(input_str)
    target = 32
    sims = [
        get_max_geodes(target, factory["costs"], (1, 0, 0, 0), (0, 0, 0, 0))
        for factory in tqdm(factories[:3])
    ]
    return str(reduce(lambda a, b: a * b, sims))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "3472"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute, test=True)


if __name__ == "__main__":
    main()
