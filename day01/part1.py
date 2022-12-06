import os

from aoc import AOC
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
    with open(f"{HERE}/test.txt", encoding="utf-8") as file:
        input_s = file.read()
    assert compute(input_s) == 2400


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 1, 1

    aoc.run_part(year, day, part, compute, auto_submit=True)


if __name__ == "__main__":
    main()
