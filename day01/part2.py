import os

from aoc import get_year_day
from aoc_api import AOC_API
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
    aoc_api = AOC_API(API_TOKEN, HERE)
    (year, day) = get_year_day()
    print(year, day)

    input_str: str = aoc_api.get_input(year, day)
    res = compute(input_str)
    print(res)


if __name__ == "__main__":
    main()
