import os
from typing import List

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def all_tokens_unique(*tokens: List[str]) -> bool:
    match = {}
    for token in tokens:
        if token in match:
            return False
        match[token] = 1
    return True


def compute(input_str: str) -> str:
    window_size = 4
    i = 0
    while i + window_size < len(input_str):
        window = input_str[i : i + window_size]
        if all_tokens_unique(*window):
            return i + window_size

        i += 1


def test() -> None:
    inputs = [
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    ]

    expected = [5, 6, 10, 11]

    for i, e in zip(inputs, expected):
        assert compute(i) == e


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 6, 1

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
