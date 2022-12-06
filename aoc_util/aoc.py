import os


def get_year_day() -> tuple[int, int]:
    cwd = os.getcwd()
    day_s = os.path.basename(cwd)
    year_s = os.path.basename(os.path.dirname(cwd))

    if not day_s.startswith('day') or not year_s.startswith('aoc'):
        raise AssertionError(f'unexpected working dir: {cwd}')

    return int(year_s[len('aoc'):]), int(day_s[len('day'):])

def _get_test_data(path = 'test.txt') -> str:
    with open(path, 'r') as file:
        return file.read()
