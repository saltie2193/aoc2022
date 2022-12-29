"""
Day 16: Proboscidea Volcanium
https://adventofcode.com/2022/day/16#part2
"""
from __future__ import annotations

import os

from aoc import AOC
from dotenv import load_dotenv

from day16.part1 import max_releasable_pressure, optimize_valves, parse

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def max_pressure_multi_path(paths: list[tuple[int, frozenset[str]]]) -> int:
    ranked_paths = sorted(paths, key=lambda x: x[0], reverse=True)
    # print(*ranked_paths, sep="\n")
    max_pressure = 0
    j = 0
    for i, (a_pressure, a_visited) in enumerate(ranked_paths):
        if i > j:
            continue
        for j, (b_pressure, b_visited) in enumerate(ranked_paths[i + 1 :], i):
            pressure = a_pressure + b_pressure
            if pressure <= max_pressure:
                break

            # paths disjoint?
            if a_visited.intersection(b_visited):
                continue

            if pressure > max_pressure:
                max_pressure = pressure

    return max_pressure


def compute(input_str: str) -> str:
    valves = parse(input_str)
    # print("valves:", *valves.items(), sep="\n")
    print(f"optimize valves (?) ...")
    optimized = optimize_valves(valves)
    # print("optimized: ", *optimized.items(), sep="\n")
    print(f"maximize released pressure ...")
    paths = max_releasable_pressure("AA", 26, optimized, intermediate_paths=True)
    return str(max_pressure_multi_path(paths))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "1707"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
