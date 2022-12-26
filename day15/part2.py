from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv
from tqdm import tqdm

from aoc_tools import manhattan_dist

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Sensor = tuple[int, int, int, int]
Position = tuple[int, int]


def get_sensor_row_coverage(row: int, sensor: Sensor) -> tuple[int, int] | None:
    (x, y) = sensor[:2]
    beacon = sensor[2:]
    dist = manhattan_dist((x, y), beacon)
    dist_row = abs(x - row)

    if dist_row > dist:
        return None

    return y - abs(dist - dist_row), y + abs(dist - dist_row)


def merge_coverage_into_row(
    coverage: tuple[int, int], row: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    if len(row) == 0:
        return [coverage]

    new_row = []
    i = 0
    for i, field in enumerate(row):
        # coverage '>' field
        if coverage[0] > field[1] + 1:
            new_row.append(field)
            continue

        # coverage '<' field
        if coverage[1] < field[0]:
            new_row.extend([coverage, *row[i:]])
            return new_row

        coverage = (min(field[0], coverage[0]), max(field[1], coverage[1]))

    new_row.append(coverage)
    return new_row


def get_row_coverage(row: int, sensors: set[Sensor]) -> list[tuple[int, int]]:
    coverage = []
    for sensor in sensors:
        sensor_coverage = get_sensor_row_coverage(row, sensor)
        if sensor_coverage is not None:
            coverage = merge_coverage_into_row(sensor_coverage, coverage)
    return coverage


def get_coverage_edge(sensor: Sensor) -> set[Position]:
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


def parse(input_str: str) -> set[Sensor]:
    sensors: set[Sensor] = set()

    for line in input_str.splitlines():
        v = line.split(" ")
        sensors.add((int(v[3][2:-1]), int(v[2][2:-1]), int(v[9][2:]), int(v[8][2:-1])))

    return sensors


def compute(input_str: str) -> str:
    sensors = parse(input_str)
    l, u = 0, 4000000

    for row_index in tqdm(range(u + 1)):
        row_coverage = get_row_coverage(row_index, sensors)
        rc = [(max(x, l), min(y, u)) for (x, y) in row_coverage if x <= u and y >= l]
        if len(rc) > 1:
            return str((rc[0][1] + 1) * 4000000 + row_index)

        if len(rc) == 1 and rc[0] != (l, u):
            return str(max(rc[0][0], l) * min(rc[0][1], u))

    return ""


@pytest.mark.skip()
def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "56000011"


def test_merge_covergae() -> None:
    row = []
    steps = [
        (1, 2),
        (4, 5),
        (2, 3),
        (3, 4),
        (10, 15),
        (7, 8),
        (4, 10),
    ]
    outs = [
        [(1, 2)],
        [(1, 2), (4, 5)],
        [(1, 3), (4, 5)],
        [(1, 5)],
        [(1, 5), (10, 15)],
        [(1, 5), (7, 8), (10, 15)],
        [(1, 15)],
    ]

    for i, step in enumerate(steps):
        row = merge_coverage_into_row(step, row)
        print(step, row)
        assert row == outs[i]


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
