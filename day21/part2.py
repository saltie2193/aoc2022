from __future__ import annotations

import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Number = tuple[str, int]
Operation = tuple[str, str, str, str]
INVERT_OP = {"+": "-", "-": "+", "*": "/", "/": "*", "=": "="}


def parse(input_str: str) -> list[Number | Operation]:
    res = []

    for line in input_str.splitlines():
        split = line.split(" ")
        key = split[0].split(":")[0]
        if len(split) == 2:
            res.append((key, int(split[1])))
            continue
        if key == "root":
            res.append((key, split[1], "=", split[3]))
            continue
        res.append((key, *split[1:]))

    return res


def rec_solve_expr(expr: tuple) -> float:
    if len(expr) == 1:
        return expr[0]

    left, op, right = expr
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


def target_in_expr(target: str, expr: tuple) -> bool:
    if expr == [target]:
        return True

    if len(expr) == 1:
        return False

    return target_in_expr(target, expr[0]) or target_in_expr(target, expr[2])


def reorder_equation(equation: tuple, target: str) -> tuple:
    if len(equation) == 1:
        raise ValueError("Expected an equation, not a value")

    left, op, right = equation
    if op != "=":
        raise ValueError(f"unsupported operator {op}")

    if target_in_expr(target, left):
        return rec_reorder_expr(left, target, right)

    if target_in_expr(target, right):
        return rec_reorder_expr(right, target, left)

    raise ValueError(f"Target '{target}' not found")


def rec_reorder_expr(expr: tuple, target: str, transformed: tuple) -> tuple:
    if expr == [target]:
        return transformed

    if len(expr) == 1:
        return transformed

    left, op, right = expr

    if target_in_expr(target, left):
        return rec_reorder_expr(left, target, (transformed, INVERT_OP[op], right))

    if target_in_expr(target, right):
        if op in ["/", "-"]:
            return rec_reorder_expr(right, target, (left, op, transformed))
        return rec_reorder_expr(right, target, (transformed, INVERT_OP[op], left))

    raise ValueError(f"Target '{target}' not found")


def compute(input_str: str) -> str:
    operations = parse(input_str)
    results: dict = {}

    while operations:
        op = operations.pop(0)
        key = op[0]
        if key == "humn":
            results[key] = ["humn"]
            continue

        if len(op) == 2:
            results[key] = [op[1]]
            continue
        key_l, key_r = op[1], op[3]

        if key_l in results and key_r in results:
            results[key] = (results[key_l], op[2], results[key_r])
            continue

        operations.append(op)
    root = results["root"]
    results["humn"] = reorder_equation(root, "humn")
    res = rec_solve_expr(results["humn"])
    return str(int(res))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "301.0"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
