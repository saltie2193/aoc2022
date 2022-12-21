from __future__ import annotations

import os
from typing import Callable

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


functions: dict[str, Callable[[int, int], int]] = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
}


def monkeys_to_str(
    monkeys: list[tuple[list[int], Callable[[int], int], Callable[[int], int]]]
) -> str:
    res = ""
    for i, (items, _, _) in enumerate(monkeys):
        res += f"{i}: {items}\n"
    return res


def parse_operation(op_str: str) -> Callable[[int], int]:
    left, op, right = op_str.split(" ")[-3:]

    fn = functions[op]
    if left == "old" and right == "old":
        return lambda x: fn(x, x)
    if left == "old":
        return lambda x: fn(x, int(right))
    if right == "old":
        return lambda x: fn(int(left), x)

    raise ValueError


def parse_get_next(lines: list[str]) -> Callable[[int], int]:
    divisor = int(lines[0].split(" ")[-1])
    success = int(lines[1].split(" ")[-1])
    fail = int(lines[2].split(" ")[-1])
    return lambda x: success if x % divisor == 0 else fail


def parse_monkey(
    monkey_str: str,
) -> tuple[list[int], Callable[[int], int], Callable[[int], int]]:
    lines = monkey_str.splitlines()
    items = [int(i.strip()) for i in lines[1][18:].split(",")]
    operation = parse_operation(lines[2])
    get_next = parse_get_next(lines[3:])

    return items, operation, get_next


def compute(input_str: str) -> str:
    monkeys = [parse_monkey(string) for string in input_str.split("\n\n")]
    inspections = [0 for _ in enumerate(monkeys)]
    rounds = 20

    for r in range(rounds):
        print(f"== Round {r} ==")
        for i, (items, operation, get_next) in enumerate(monkeys):
            print(f"Monkey {i}:")
            monkeys[i] = ([], operation, get_next)
            inspections[i] += len(items)
            for item in items:
                worry = operation(item) // 3
                print(f"    worry {item} -> {worry}")
                next_monkey = get_next(worry)
                print(f"    throw {worry} to {next_monkey}")
                monkeys[next_monkey][0].append(worry)
        print(monkeys_to_str(monkeys))

    x = sorted(enumerate(inspections), key=lambda a: a[1])
    return str(x[-1][1] * x[-2][1])


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "10605"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
