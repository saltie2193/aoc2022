from __future__ import annotations

import os
from typing import Optional

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def parse(input_str: str) -> list[tuple[str, int]]:
    lines = [line.split(" ") for line in input_str.splitlines()]
    return [(a[0], int(a[1])) if len(a) > 1 else (a[0], 0) for a in lines]


def tick(
    cycle: int,
    actions: list[tuple[str, int]],
    registers: dict,
    wait: Optional[int] = None,
) -> tuple[int, list[tuple[str, int]], dict, Optional[int]]:
    operation, number = actions[0]
    print(cycle, (operation, number), registers, wait)

    if operation == "noop":
        return cycle + 1, actions[1:], {**registers}, None

    if operation == "addx":
        if wait is None:
            return cycle + 1, actions, {**registers}, 0

        if wait <= 0:
            registers["x"] += number
            return cycle + 1, actions[1:], {**registers}, None

        return cycle + 1, actions, {**registers}, wait - 1

    raise ValueError(f"Unknown operation {operation}")


def compute(input_str: str) -> str:
    actions = parse(input_str)
    registers = dict(x=1)
    cycles = []
    cycle = 1
    wait = None
    res = 0
    while len(actions) > 0:
        cycles.append((cycle, registers, wait))
        cycle, actions, registers, wait = tick(cycle, actions, registers, wait)
        if cycle in [20, 60, 100, 140, 180, 220]:
            res += cycle * registers["x"]
    return str(res)


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "13140"


def main():
    API_TOKEN = ""
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
