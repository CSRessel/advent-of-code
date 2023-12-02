from functools import reduce
from typing import DefaultDict
import operator


TEST = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

reqs = {
    "red": 12,
    "green": 13,
    "blue": 14,
    }

def check_game_reps(game_reps: str) -> bool:
    for game in game_reps.split(";"):
        for observation in game.split(","):
            count, color = observation.strip().split(" ")
            if reqs[color] < int(count):
                return False
    return True

def solve(input):
    games = []
    for line in input.splitlines():
        id = line[line.index("Game") + 5:line.index(":")]
        reps = line[line.index(":") + 2:]
        if check_game_reps(reps):
            games.append(int(id))
    return sum(games)

def solve_bonus(input):
    game_powers = []
    for line in input.splitlines():
        reps = line[line.index(":") + 2:]
        game_mins = DefaultDict(int)
        for game in reps.split(";"):
            for observation in game.split(","):
                count, color = observation.strip().split(" ")
                if game_mins[color] < int(count):
                    game_mins[color] = int(count)
        game_powers.append(reduce(operator.mul, [count for count in game_mins.values()]))
    return sum(game_powers)

def test():
    assert solve(TEST) == 8
    assert solve_bonus(TEST) == 2286
    with open("input", "r") as f:
        print(solve(f.read()))
    with open("input", "r") as f:
        print(solve_bonus(f.read()))
def main():
    test()

if __name__ == "__main__":
  main()
