from __future__ import annotations

import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def parse(input_str: str) -> set[tuple[int, int, int]]:
    return {tuple(map(int, line.split(","))) for line in input_str.splitlines()}


def get_neighbors(cube: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    x, y, z = cube
    neighbors = {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }
    return neighbors


def get_neighbors_empty(
    cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]
) -> set[tuple[int, int, int]]:
    return get_neighbors(cube).difference(cubes)


def get_neighbors_cubes(
    cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]
) -> set[tuple[int, int, int]]:
    return cubes.intersection(get_neighbors(cube))


def count_free_surfaces(
    cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]
) -> int:
    return len(get_neighbors_empty(cube, cubes))


def count_blocked_surfaces(
    cube: tuple[int, int, int], cubes: set[tuple[int, int, int]]
) -> int:
    return len(get_neighbors_cubes(cube, cubes))


def get_surface_area(droplet: set[tuple[int, int, int]]) -> int:
    res = 0

    for cube in droplet:
        res += count_free_surfaces(cube, droplet)

    return res


def form_droplet(
    cube: tuple[int, int, int],
    cubes: set[tuple[int, int, int]],
    droplet: set[tuple[int, int, int]],
) -> tuple[set[tuple[int, int, int]], set[tuple[int, int, int]]]:
    droplet.add(cube)

    x, y, z = cube
    neighbors = get_neighbors(cube)

    for neighbor in neighbors:
        if neighbor in droplet:
            continue

        if neighbor in cubes:
            droplet, cubes = form_droplet(
                neighbor, cubes.difference({neighbor, cube}), droplet
            )

        cubes = cubes.difference({neighbor, cube})

    return droplet, cubes


def form_air2(
    cube: tuple[int, int, int],
    cubes: set[tuple[int, int, int]],
    xyz_min: tuple[int, int, int],
    xyz_max: tuple[int, int, int],
) -> set[tuple[int, int, int]]:
    air = set()

    to_visit = [cube]

    while len(to_visit) > 0:
        node = to_visit.pop()
        air.add(node)
        for (x, y, z) in get_neighbors(node):
            if (x, y, z) in air or (x, y, z) in cubes:
                continue
            if x < xyz_min[0] or y < xyz_min[1] or z < xyz_min[2]:
                continue
            if x > xyz_max[0] or y > xyz_max[1] or z > xyz_max[2]:
                continue
            if (x, y, z) in to_visit:
                continue

            to_visit.append((x, y, z))

    return air


def compute(input_str: str) -> str:
    cubes = set(parse(input_str))

    xyz_min = tuple(map(lambda x: min(x) - 1, zip(*cubes)))
    xyz_max = tuple(map(lambda x: max(x) + 1, zip(*cubes)))

    air = form_air2(xyz_min, cubes, xyz_min, xyz_max)
    return str(sum(len(get_neighbors_cubes(cube, cubes)) for cube in air))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "58"


def test_simple() -> None:
    input_s = """\
1,1,1
2,1,1
"""
    assert compute(input_s) == "10"


def test_parse() -> None:
    input_s = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

    out = {
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5),
    }

    assert parse(input_s) == out


def test_neighbors() -> None:
    cubes = {
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5),
    }

    for cube in cubes:
        c = get_neighbors_cubes(cube, cubes)
        e = get_neighbors_empty(cube, cubes)

        assert len(e) + len(c) == 6


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
