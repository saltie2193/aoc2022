from __future__ import annotations

import os

from dotenv import load_dotenv
from tqdm import tqdm

from aoc_tools import manhattan_dist

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def get_row_coverage(
    row: int, sensor: tuple[int, int, int, int]
) -> tuple[int, int] | None:
    (x, y) = sensor[:2]
    beacon = sensor[2:]
    dist = manhattan_dist((x, y), beacon)
    dist_row = abs(x - row)

    if dist_row > dist:
        return None

    return y - abs(dist - dist_row), y + abs(dist - dist_row)


def get_coverage_edge(sensor: tuple[int, int, int, int]) -> set[tuple[int, int]]:
    (x, y) = sensor[:2]
    beacon = sensor[2:]

    dist = manhattan_dist((x, y), beacon)
    print(dist)
    coverage = set()

    for i in tqdm(range(dist + 1)):
        j = dist - i
        coverage.update(
            [
                (x + i, y + j),
                (x + i, y - j),
                (x - i, y + j),
                (x - i, y - j),
            ]
        )
    return coverage


def parse(input_str: str) -> set[tuple[int, int, int, int]]:
    sensors: set[tuple[int, int, int, int]] = set()

    for line in input_str.splitlines():
        v = line.split(" ")
        sensors.add((int(v[3][2:-1]), int(v[2][2:-1]), int(v[9][2:]), int(v[8][2:-1])))

    return sensors


def compute(input_str: str) -> str:
    sensors = parse(input_str)
    beacons = {sensor[2:] for sensor in sensors}
    row = 2000000
    lower, upper = 0, 0

    for sensor in sensors:
        res = get_row_coverage(row, sensor)
        if res is None:
            continue
        a, b = res
        if a < lower:
            lower = a

        if b > upper:
            upper = b

    # magic
    beacons_in_res = [
        beacon
        for beacon in beacons
        if beacon[0] == row and beacon[1] >= lower and beacon[1] <= upper
    ]
    print(lower, upper, "->", upper - lower)
    return str(upper - lower + 1 - len(beacons_in_res))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "1"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
