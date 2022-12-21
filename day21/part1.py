from __future__ import annotations

import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Number = tuple[str, int]
Operation = tuple[str, str, str, str]


def parse(input_str: str) -> list[Number | Operation]:
    res = []
    for line in input_str.splitlines():
        split = line.split(" ")
        key = split[0].split(":")[0]
        if len(split) == 2:
            res.append((key, int(split[1])))
            continue
        res.append((key, *split[1:]))

    return res


def rec_solve_expr(_list: list) -> float:
    if len(_list) == 1:
        return _list[0]

    left, op, right = _list
    solved_left = rec_solve_expr(left)
    solved_right = rec_solve_expr(right)
    if op == "+":
        return solved_left + solved_right
    if op == "-":
        return solved_left - solved_right
    if op == "*":
        return solved_left * solved_right
    if op == "/":
        return solved_left / solved_right

    raise ValueError(f"Unknown operation '{op}'")


def compute(input_str: str) -> str:
    operations = parse(input_str)
    # print(*operations, sep="\n")
    results: dict = {}

    while operations:
        op = operations.pop(0)
        key = op[0]
        if len(op) == 2:
            results[key] = [op[1]]
            continue

        key_l, key_r = op[1], op[3]
        if key_l in results and key_r in results:
            results[key] = [results[key_l], op[2], results[key_r]]
            continue

        operations.append(op)

    return str(int(rec_solve_expr(results["root"])))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "152"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
