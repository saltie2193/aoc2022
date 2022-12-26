"""
Day 24: Blizzard Basin - Part 2
https://adventofcode.com/2022/day/24#part2
"""
from __future__ import annotations

import os

from aoc import AOC
from dotenv import load_dotenv

from day24.part1 import (
    parse,
    find_path_length,
    Position,
    Weather,
    predict_weather_n,
)

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def find_path_length_for_path(
        path: list[Position], weather: Weather, magic: int
) -> int:
    distances = []
    for i in range(len(path) - 1):
        start, end = path[i: i + 2]
        res = find_path_length(start, end, weather, magic, sum(distances))
        print(f"{start} -> {end}: {res}")
        distances.append(res)
    return sum(distances)


def compute(input_str: str) -> str:
    start, end, blizzards, maxs = parse(input_str)
    magic = (maxs[0] - 1) * (maxs[1] - 1)
    path = [start, end, start, end]
    print("predicting weather")
    weather = predict_weather_n(blizzards, maxs)

    print("start solving")
    res = find_path_length_for_path(path, weather, magic)

    return str(res)


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "54"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
