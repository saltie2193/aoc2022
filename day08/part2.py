import os
from typing import Optional

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def trees_to_str(visible: list[list[int]]):
    res = ""
    for row in visible:
        for tree in row:
            res += str(tree)
        res += "\n"

    return res


def compute_scenic_score(tree: tuple[int, int], height_map: list[list[int]]) -> int:
    up, down, left, right = 0, 0, 0, 0
    height = height_map[tree[0]][tree[1]]

    while tree[0] + down + 1 < len(height_map):
        down += 1
        if height <= height_map[tree[0] + down][tree[1]]:
            break

    while tree[0] - (up + 1) >= 0:
        up += 1
        if height <= height_map[tree[0] - up][tree[1]]:
            break

    while tree[1] + right + 1 < len(height_map):
        right += 1
        if height <= height_map[tree[0]][tree[1] + right]:
            break

    while tree[1] - (left + 1) >= 0:
        left += 1
        if height <= height_map[tree[0]][tree[1] - left]:
            break

    print(f"{tree}: {height=}, {up=}, {down=}, {left=}, {right=}")

    return up * down * left * right


def compute_scenic_scores(height_map: list[list[int]]) -> list[list[int]]:
    res = []
    for i, row in enumerate(height_map):
        res.append([])
        for j, tree in enumerate(row):
            res[i].append(compute_scenic_score((i, j), height_map))

    return res


def compute(input_str: str) -> str:
    matrix = [[int(c) for c in line] for line in input_str.splitlines()]
    scores = compute_scenic_scores(matrix)
    return str(max(max(row) for row in scores))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "8"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
