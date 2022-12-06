import os

from aoc import AOC
from dotenv import load_dotenv

load_dotenv("../.venv")
API_TOKEN = os.getenv("API_TOKEN")

HERE = os.path.dirname(os.path.abspath(__file__))


def compute(input_str: str) -> str:
    elfs = map(lambda elf: elf.splitlines(), input_str.split("\n\n"))
    calories = list(map(lambda elf: sum([int(line) for line in elf]), elfs))
    calories.sort(reverse=True)
    return sum(calories[0:3])


def test() -> None:
    input_s = ""
    with open(f"{HERE}/test.txt") as file:
        input_s = file.read()
    assert compute(input_s) == 45000


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 1, 2

    aoc.run_part(year, day, part, compute, auto_submit=True)


if __name__ == "__main__":
    main()
