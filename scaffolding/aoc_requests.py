"""
Based Off: https://github.com/LiquidFun/adventofcode

To use this script, you need to have a file named
"session.cookie" in the same folder as this script.

It should contain a single line, the "session" cookie
when logged in to https://adventofcode.com. Just
paste it in there.

Then install the requirements as listed here:
    pip install requests
"""
import functools
import itertools
import math
import time
from collections import namedtuple
from functools import cache
from pathlib import Path
import re
import json
from typing import Any, Literal

import requests

# This results in the parent directory of the script directory, the year directories should be here
AOC_DIR = Path(__file__).absolute().parent.parent

# This results in the parent folder of the script file
AOC_REQUESTS_DIR = Path(__file__).absolute().parent

# Cache path is a subfolder of the AOC folder, it includes the personal leaderboards for each year
CACHE_DIR = AOC_REQUESTS_DIR / ".requests_cache"

# Path to the cookie session file
SESSION_COOKIE_PATH = AOC_DIR / "session.cookie"

# The year and day pattern to detect directories. For example, if your day folders are
# called "day1" to "day25" then set the pattern to r"day\d{1,2}". The script extracts
# a number from the folder and tries to guess its day that way.
YEAR_PATTERN = r"\d{4}"
DAY_PATTERN = r"\d{2}"

DayScores = namedtuple("DayScores", ["time1", "rank1", "score1", "time2", "rank2", "score2"], defaults=[None] * 3)


# URL for the personal leaderboard (same for everyone)
PERSONAL_LEADERBOARD_URL = "https://adventofcode.com/{year}/leaderboard/self"

def parse_leaderboard(leaderboard_path: Path) -> dict[int, DayScores]:
    no_stars = "You haven't collected any stars... yet."
    start = '<span class="leaderboard-daydesc-both"> *Time *Rank *Score</span>\n'
    end = "</pre>"
    with open(leaderboard_path) as file:
        html = file.read()
        if no_stars in html:
            return {}
        matches = re.findall(rf"{start}(.*?){end}", html, re.DOTALL | re.MULTILINE)
        assert len(matches) == 1, f"Found {'no' if len(matches) == 0 else 'more than one'} leaderboard?!"
        table_rows = matches[0].strip().split("\n")
        leaderboard = {}
        for line in table_rows:
            day, *scores = re.split(r"\s+", line.strip())
            # replace "-" with None to be able to handle the data later, like if no score existed for the day
            scores = [s if s != "-" else None for s in scores]
            assert len(scores) in (3, 6), f"Number scores for {day=} ({scores}) are not 3 or 6."
            leaderboard[int(day)] = DayScores(*scores)
        return leaderboard

def request_leaderboard(year: int) -> dict[int, Any]:
    leaderboard_path = CACHE_DIR / f"leaderboard{year}.html"
    if leaderboard_path.exists():
        leaderboard = parse_leaderboard(leaderboard_path)
        less_than_30mins = time.time() - leaderboard_path.lstat().st_mtime < 60 * 30
        if less_than_30mins:
            print(f"Leaderboard for {year} is younger than 30 minutes, skipping download in order to avoid DDOS.")
            return leaderboard
        has_no_none_values = all(itertools.chain(map(list, leaderboard.values())))
        if has_no_none_values and len(leaderboard) == 25:
            print(f"Leaderboard for {year} is complete, no need to download.")
            return leaderboard
    with open(SESSION_COOKIE_PATH) as cookie_file:
        session_cookie = cookie_file.read().strip()
        assert len(session_cookie) == 128, f"Session cookie is not 128 characters long, make sure to remove the prefix!"
        data = requests.get(
            PERSONAL_LEADERBOARD_URL.format(year=year),
            headers={"User-Agent": "https://github.com/LiquidFun/adventofcode by Brutenis Gliwa"},
            cookies={"session": session_cookie},
        ).text
        leaderboard_path.parent.mkdir(exist_ok=True, parents=True)
        with open(leaderboard_path, "w") as file:
            file.write(data)
    return parse_leaderboard(leaderboard_path)

class HTMLTag:
    def __init__(self, parent: "HTML", tag: str, closing: bool = True, **kwargs):
        self.parent = parent
        self.tag = tag
        self.closing = closing
        self.kwargs = kwargs
        attributes = "".join(f' {k}="{v}"' for k, v in self.kwargs.items())
        self.parent.push(f"<{self.tag}{attributes}>", depth=self.closing)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        if self.closing:
            self.parent.push(f"</{self.tag}>", depth=-self.closing)
class HTML:
    tags: list[str] = []
    depth = 0

    def push(self, tag: str, depth=0):
        if depth < 0:
            self.depth += depth
        self.tags.append("  " * self.depth + tag)
        if depth > 0:
            self.depth += depth

    def tag(self, tag: str, closing: bool = True, **kwargs):
        return HTMLTag(self, tag, closing, **kwargs)

    def __str__(self):
        return "\n".join(self.tags)

def main():
    pass

if __name__ == "__main__":
    main()
