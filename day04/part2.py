import os

from aoc_api import AOC_API
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def compute(input_str: str) -> str:
    count = 0
    for line in input_str.splitlines():
        r0, r1 = [(int(a), int(b)) for a, b in [r.split("-") for r in line.split(",")]]
        if r0[0] <= r1[1] and r0[1] >= r1[1]:
            count += 1
        elif r1[0] <= r0[1] and r1[1] >= r0[1]:
            count += 1

    return count


def test() -> None:
    input_s = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    assert compute(input_s) == 2


def main():
    aoc_api = AOC_API(API_TOKEN, HERE)
    year, day, part = 2022, 4, 2

    input_str: str = aoc_api.get_input(year, day)
    answer = compute(input_str)
    print(answer)
    res = aoc_api.submit_solution(year, day, part, answer)
    print(res)


if __name__ == "__main__":
    main()