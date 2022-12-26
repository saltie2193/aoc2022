def manhattan_dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    return sum(abs(_a - _b) for _a, _b in zip(a, b))


def test_manhattan_dist() -> None:
    tests = [
        ((0, 0), [
            (0, 0, 0), (0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1),
            (1, 1, 2), (1, -1, 2), (-1, 1, 2), (-1, -1, 2),
        ])
    ]

    for start, cases in tests:
        for x, y, res in cases:
            assert manhattan_dist(start, (x, y)) == res
