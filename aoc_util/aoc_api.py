import os
import re
from enum import IntEnum, auto
from typing import Optional, Tuple

import requests


class SubmitResult(IntEnum):
    TOO_QUICK = auto()
    WRONG = auto()
    RIGHT = auto()
    ALREADY_DONE = auto()
    UNEXPECTED = auto()


TOO_QUICK = re.compile(r"You gave an answer too recently.*to wait\.")
WRONG = re.compile(r"That's not the right answer.*?.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


class AOC_API:
    session_cookie: str
    cache_dir: str

    def __init__(self, session_cookie: str, cache_dir: str) -> None:
        self.session_cookie = session_cookie
        self.cache_dir = cache_dir

    def _get_base_url(self, year, day) -> str:
        return f"https://adventofcode.com/{year}/day/{day}"

    def _get_cookies(self) -> dict[str, str]:
        return dict(session=self.session_cookie)

    def _get_input(self, year: int, day: int) -> str:
        url = f"{self._get_base_url(year, day)}/input"
        res = requests.get(url, cookies=self._get_cookies(), timeout=5)
        return res.text

    def get_input(self, year: int, day: int) -> str:
        print(self.cache_dir)
        res: str
        path_to_file = f"{self.cache_dir}/input.txt"
        if os.path.exists(path_to_file):
            with open(path_to_file, "r", encoding="utf-8") as file:
                return file.read()
        else:
            res = self._get_input(year, day)
            with open(path_to_file, "w", encoding="utf-8") as file:
                file.write(res)
            return res

    def _post_answer(
        self, year: int, day: int, part: int, answer: str
    ) -> requests.Response:
        url = f"{self._get_base_url(year, day)}/answer"
        payload = dict(level=part, answer=answer)

        return requests.post(url, payload, cookies=self._get_cookies(), timeout=5)

    def submit_solution(
        self, year: int, day: int, part: int, answer: str
    ) -> Tuple[SubmitResult, Optional[int]]:
        contents = self._post_answer(year, day, part, answer)

        for error_regex, ret in zip(
            (WRONG, TOO_QUICK, ALREADY_DONE),
            (SubmitResult.WRONG, SubmitResult.TOO_QUICK, SubmitResult.ALREADY_DONE),
        ):
            error_match = error_regex.search(contents.text)
            if error_match:
                return (ret, None)

        if RIGHT in contents:
            print(f"\033[42m{RIGHT}\033[m")
            return (SubmitResult.RIGHT, None)
        else:
            # unexpected output?
            print(contents.text)
            return (SubmitResult.UNEXPECTED, None)
