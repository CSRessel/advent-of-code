import re

TEST = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

TEST_BONUS = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineightseven2
zoneeight234
7pqrstsixteen
"""

def clean_input(input):
    return input.strip().splitlines()
def lfind_digi(s):
    for c in s:
        if c.isdigit():
            return c
    return ''

WORD_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
    }
def lfind_word_or_digi(s):
    matchgroup = re.match(r'.*?([1-9]|one|two|three|four|five|six|seven|eight|nine)', s)
    if matchgroup:
        num = matchgroup.group(1)
        if num.isdigit():
            return num
        else:
            return WORD_MAP[num]
    return ''
def rfind_word_or_digi(s):
    matchgroup = re.match(r'.*([1-9]|one|two|three|four|five|six|seven|eight|nine)', s)
    if matchgroup:
        num = matchgroup.group(1)
        if num.isdigit():
            return num
        else:
            return WORD_MAP[num]
    return ''

def solve(input):
    nums = [f'{lfind_digi(l)}{lfind_digi(reversed(l))}' for l in clean_input(input)]
    ans = sum([int(n) for n in nums])
    return ans
def solve_bonus(input):
    nums = [f'{lfind_word_or_digi(l)}{rfind_word_or_digi(l)}' for l in clean_input(input)]
    ans = sum([int(n) for n in nums])
    return ans

def test():
    ans = solve(TEST)
    assert ans == 142
def test_bonus():
    ans = solve_bonus(TEST_BONUS)
    assert ans == 281

def main():
    test()
    test_bonus()

    with open('input') as f:
        fileinput = f.read()
    ans = solve(fileinput)
    print("Part 1")
    print(ans)

    with open('input.bonus') as f:
        fileinput = f.read()
    ans = solve_bonus(fileinput)
    print("Part 2")
    print(ans)

if __name__ == "__main__":
    main()
