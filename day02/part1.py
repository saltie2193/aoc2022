"""
Day 2: Rock Paper Scissors - Part 1
https://adventofcode.com/2022/day/2
"""
import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

# A(1): Rock , B(2): Paper, C(3): Scissor
#
#    1 2 3
#   ------
# 1| 1 0 2
# 2| 2 1 0
# 3| 0 2 1
#
# [0, 1, 2]

abc_from_xyz = {"X": "A", "Y": "B", "Z": "C"}
value_from_token = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
map_winner = {
    "AA": 0,
    "AB": 1,
    "AC": -1,
    "BA": -1,
    "BB": 0,
    "BC": 1,
    "CA": 1,
    "CB": -1,
    "CC": 0,
}
map_token_worth = {"A": 1, "B": 2, "C": 3}


def calc_player(a: str, b: str) -> int:
    points: int = map_token_worth[a]
    if map_winner[a + b] < 0:
        return points + 6
    elif map_winner[a + b] == 0:
        return points + 3
    else:
        return points


def calc_round(a: str, b: str) -> tuple[int, int]:
    # _a = abc_from_xyz[a]
    _b = abc_from_xyz[b]
    return calc_player(a, _b), calc_player(_b, a)


def compute(input_str: str) -> str:
    return str(
        sum(
            calc_round(a, b)[1]
            for a, b in [line.split() for line in input_str.splitlines()]
        )
    )


def test_token_worth() -> None:
    tokens = ["A", "B", "C"]
    expected = [1, 2, 3]

    for i, token in enumerate(tokens):
        assert map_token_worth[token] == expected[i]


def test_calc_player() -> None:
    input_s = ["A X", "A Y", "A Z", "B X", "B Y", "B Z", "C X", "C Y", "C Z"]
    expected = [4, 1, 7, 8, 5, 2, 3, 9, 6]

    for i, x in zip(input_s, expected):
        a, b = i.split(" ")
        assert calc_player(a, abc_from_xyz[b]) == x


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "15"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 2, 1

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
