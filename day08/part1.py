import os
from typing import Optional

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def transpose_matrix(matrix: list[list]) -> list[list]:
    return list(map(list, zip(*matrix)))


def visible_to_str(visible: list[list[bool]]):
    res = ""
    for row in visible:
        for tree in row:
            if tree:
                res += "*"
            else:
                res += " "
        res += "\n"

    return res


def trees_to_str(visible: list[list[int]]):
    res = ""
    for row in visible:
        for tree in row:
            res += str(tree)
        res += "\n"

    return res


def mark_visible_row(
    row: list[int], visible: Optional[list[bool]] = None
) -> list[bool]:
    if visible is None:
        visible = [False for _ in range(len(row))]

    min_height = -1
    for i, height in enumerate(row):
        if height > min_height:
            visible[i] = True
            min_height = height
    visible = list(reversed(visible))

    min_height = -1
    for i, height in enumerate(reversed(row)):
        if height > min_height:
            min_height = height
            visible[i] = True
    return list(reversed(visible))


def mark_visible_matrix(
    matrix: list[list[int]], visible: Optional[list[list[bool]]] = None
) -> list[list[bool]]:
    if visible is None:
        visible = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for i, row in enumerate(matrix):
        visible[i] = mark_visible_row(row, visible[i])

    return visible


def compute(input_str: str) -> str:
    matrix = [[int(c) for c in line] for line in input_str.splitlines()]
    step1 = mark_visible_matrix(matrix)
    step2 = mark_visible_matrix(transpose_matrix(matrix), transpose_matrix(step1))
    return str(sum(sum(row) for row in step2))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "21"


def test_transpose_matrix() -> None:
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    res = [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

    assert transpose_matrix(matrix) == res


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
