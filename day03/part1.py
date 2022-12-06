import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def get_common(input_str: str) -> str:
    half = len(input_str) // 2
    a, b = input_str[:half], input_str[half:]
    in_a = {}
    in_b = {}
    for _a, _b in zip(a, b):
        if _a == _b:
            return _a
        if _b in in_a:
            return _b
        if _a in in_b:
            return _a

        in_a[_a] = True
        in_b[_b] = True


def gert_priority(c: str) -> int:
    value = ord(c)
    if value >= 97:
        return value - 96
    if value >= 65:
        return value - 38


def compute(input_str: str) -> str:
    commons = [get_common(line) for line in input_str.splitlines()]
    print(commons)
    prios = list(map(gert_priority, commons))
    print(prios)
    return sum(prios)


def test() -> None:
    input_s = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
    assert compute(input_s) == 157


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 3, 1

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
