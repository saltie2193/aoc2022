from __future__ import annotations
from typing import Dict, Optional, Union
import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


class File(object):
    name: str
    size: int
    folder = False
    parent: Folder

    def __init__(self, name: str, size, parent) -> None:
        self.name = name
        self.size = size
        self.parent = parent

    @property
    def path(self):
        return self.parent.path + "/" + self.name


class Folder(object):
    name: str
    items: Dict
    folder = True
    parent: Optional[Folder]

    def __init__(self, name: str, parent: Optional[Folder] = None) -> None:
        self.name = name
        self.parent = parent
        self.items = {}

    @property
    def size(self):
        return sum(c.size for c in self.items.values())

    @property
    def path(self):
        if self.parent is None:
            return self.name
        return self.parent.path + "/" + self.name

    def go_to_root(self):
        if self.parent is None:
            return self
        return self.parent.go_to_root()

    def get_all_existing_folders(self):
        items_local = {v.path: v for k, v in self.items.items() if v.folder is True}
        items = list(items_local.values())
        for item in items:
            for i in item.get_all_existing_folders().values():
                items_local[i.path] = i
        return items_local


    def cd(self, path: str) -> Optional[Folder]:
        if path == "..":
            return self.parent

        return self.items.get(path)

    def add_item(self, item: Union[Folder, File]):
        if item.name in self.items:
            print(f"item '{item.name}' already exists! Overwriting it!")
            pass
        self.items[item.name] = item


def parse_cd(line: str, tree: Folder):
    _, _, target = line.split(" ")
    if target == "..":
        return tree.parent

    if target == "/":
        return tree.go_to_root()

    if not target in tree.items:
        print(f"dir {target} does not exist in {tree.path}!")
        folder = Folder(target, tree)
        tree.add_item(folder)
        return folder
    return tree.cd(target)


def parse(input_str: str) -> Folder:
    root = Folder("/")
    current = root
    lines = input_str.splitlines()
    for line in lines:
        if line.startswith("$ cd"):
            current = parse_cd(line, current)
            continue

        if line.startswith("$ ls"):
            continue

        if line.startswith("dir"):
            _, name = line.split(" ")
            current.add_item(Folder(name, current))
            continue

        size, name = line.split(" ")
        current.add_item(File(name, int(size), current))

    return root


def compute(input_str: str) -> str:
    max_space = 70000000
    required_space = 30000000
    root = parse(input_str)
    folders = list(root.get_all_existing_folders().values())
    free_space = max_space - root.size
    folders.sort(key=lambda a: a.size)
    for folder in folders:
        if folder.size > required_space - free_space:
            return str(folder.size)
    # return str(sum(folder.size for folder in folders if folder.size < 100000))


def test() -> None:
    input_s = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    assert compute(input_s) == "24933642"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 7, 2

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()
