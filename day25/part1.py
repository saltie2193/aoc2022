from __future__ import annotations

import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

DIGIT_SNAFU_TO_BASE10 = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
DIGIT_BAS10 = _TO_SNAFU = "=-012"


def snafu_to_int(snafu: str) -> int:
    res = 0
    for i, c in enumerate(reversed(snafu)):
        res += DIGIT_SNAFU_TO_BASE10[c] * 5 ** i
    return res


def base10_to_snafu(number: int) -> str:
    base = 5
    factor = 1
    while number / (base ** factor) > 1:
        factor += 1
    factor -= 1

    digits = []
    rem = number
    while rem != 0:
        rem, d = divmod(rem + 2, 5)
        digits.append("=-012"[d])

    return "".join(reversed(digits))


def compute(input_str: str) -> str:
    return str(base10_to_snafu(sum(map(snafu_to_int, input_str.splitlines()))))


def test_snafu_to_int() -> None:
    tests = [
        ("1", 1),
        ("2", 2),
        ("1=", 3),
        ("1-", 4),
        ("10", 5),
        ("11", 6),
        ("12", 7),
        ("2=", 8),
        ("2-", 9),
        ("20", 10),
        ("1=0", 15),
        ("1-0", 20),
        ("1=11-2", 2022),
        ("1-0---0", 12345),
        ("1121-1110-1=0", 314159265),
        ("1=-0-2", 1747),
        ("12111", 906),
        ("2=0=", 198),
        ("21", 11),
        ("2=01", 201),
        ("111", 31),
        ("20012", 1257),
        ("112", 32),
        ("1=-1=", 353),
        ("1-12", 107),
        ("12", 7),
        ("1=", 3),
        ("122", 37)
    ]

    for i, o in tests:
        assert snafu_to_int(i) == o


def test_sum_decimal() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert sum(map(snafu_to_int, input_s.splitlines())) == 4890


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "2=-1=0"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
