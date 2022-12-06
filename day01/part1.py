import os

from aoc_api import AOC_API
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def compute(input_str: str) -> str:
    return max(
        sum(int(line) for line in elf.splitlines()) for elf in input_str.split("\n\n")
    )


def test() -> None:
    input_s = ""
    with open(f"{HERE}/test.txt") as file:
        input_s = file.read()
    assert compute(input_s) == 2400


def main():
    aoc_api = AOC_API(API_TOKEN, HERE)
    year, day, part = 2022, 1, 1

    input_str: str = aoc_api.get_input(year, day)
    answer = compute(input_str)
    res = aoc_api.submit_solution(year, day, part, answer)
    print(res)


if __name__ == "__main__":
    main()
