from __future__ import annotations

import json
import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def parse_list(packet_str: str, offset: int = 0) -> tuple[list, int]:
    _l = []
    i = offset
    while i < len(packet_str):
        token = packet_str[i]
        print(token)
        if token == "[":
            sub, off = parse_list(packet_str, i + 1)
            _l.append(sub)
            i = off + 1
            continue

        if token == "]":
            return _l, i

        if token == ",":
            i += 1
            continue

        _l.append(int(token))
        i += 1
        # print(_l)

    return _l, i


def parse_packet(packet_str: str) -> list:
    return json.loads(packet_str)
    packet, _ = parse_list(packet_str)
    print(packet)
    return packet[0]


def parse(input_str: str) -> list[tuple[list | int, list | int]]:
    res = []
    for pairs in input_str.split("\n\n"):
        packets = []
        for packet in pairs.split("\n"):
            packets.append(parse_packet(packet))

        res.append(tuple(packets))
    return res


def compare(a: list | int, b: list | int) -> int:
    if isinstance(a, int) and isinstance(b, int):
        return max(min(1, a - b), -1)

    if isinstance(a, list) and isinstance(b, list):
        for _a, _b in zip(a, b):
            r = compare(_a, _b)
            if r != 0:
                return r
        if len(a) < len(b):
            return -1

        if len(a) > len(b):
            return 1

        return 0

    if isinstance(a, list):
        return compare(a, [b])

    return compare([a], b)


def compute(input_str: str) -> str:
    pairs: list[tuple[list | int, list | int]] = parse(input_str)
    print(pairs)
    mapped = list(map(lambda p: compare(*p), pairs))
    print(mapped)
    s = 0
    for i, m in enumerate(mapped):
        if m < 0:
            s += i + 1
    return str(s)


def test_parse_packet() -> None:
    input_str = "[1,1,3,1,1]"
    exp = [1, 1, 3, 1, 1]

    packet = parse_packet(input_str)
    assert packet == exp


def test_parse_packet_empty() -> None:
    input_str = "[]"
    exp = []
    assert parse_packet(input_str) == exp


def test_parse_packet_single() -> None:
    input_str = "[3]"
    exp = [3]
    assert parse_packet(input_str) == exp


def test_parse_packet_nested() -> None:
    input_str = "[1,[2,[3,[4,[5,6,7]]]],8,9]"
    exp = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
    packet = parse_packet(input_str)
    print(packet)
    assert packet == exp


def test_compare_list_equal() -> None:
    inp = ([1, 1, 3, 1, 1], [1, 1, 3, 1, 1])

    assert compare(*inp) == 0


def test_compare_list_not_equal() -> None:
    ins = [([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]), ([1, 1, 5, 1, 1], [1, 1, 3, 1, 1])]
    outs = [-1, 1]

    for i, o in zip(ins, outs):
        assert compare(*i) == o


def test_compare_list_int_equal() -> None:
    inp = ([1], [[1]])

    assert compare(*inp) == 0


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "13"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()
