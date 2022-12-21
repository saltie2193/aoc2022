from __future__ import annotations

import os
from typing import Optional

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def get_screen(active: list[int], width: int, lines: int) -> str:
    res = ""
    for i in range(width * lines):
        if i != 0 and i % width == 0:
            res += "\n"

        if i in active:
            res += "#"
        else:
            res += "."

    return res


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
    # print(cycle, (operation, number), registers, wait)

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
    cycle = 1
    wait = None
    active = []
    width = 40
    while len(actions) > 0:
        if (cycle - 1) % width in range(registers["x"] - 1, registers["x"] + 2):
            active.append(cycle - 1)
        cycle, actions, registers, wait = tick(cycle, actions, registers, wait)

    print(get_screen(active, width, 6))

    return str(get_screen(active, width, 6))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    out = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
    assert compute(input_s) == out


def main():
    API_TOKEN = ""
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
