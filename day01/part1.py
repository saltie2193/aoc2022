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
    input_s = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
    assert compute(input_s) == 24000


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 1, 1

    aoc.run_part(year, day, part, compute, auto_submit=True)


if __name__ == "__main__":
    main()
