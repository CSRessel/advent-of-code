#!/bin/bash

read -d '' TEST <<- EOF
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
EOF

pysoln="import math; import sys; data = sys.stdin.readlines();
splits = list(map(lambda s: s.split(' | '), data))
sets = [(set(card[0][card[0].index(': ') + 2:].split()), set(card[1].split())) for card in splits]
print(sum([int(math.pow(2, len(winners & numbers) - 1)) for winners, numbers in sets]))"

echo "test 1"
echo "$TEST" | python -c "$pysoln"

echo
echo "part 1"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cat $SCRIPT_DIR/input | python -c "$pysoln"

pysoln_bonus="import math; import sys; data = sys.stdin.readlines();
splits = list(map(lambda s: s.split(' | '), data))
sets = [(set(card[0][card[0].index(': ') + 2:].split()), set(card[1].split())) for card in splits]
per_card_winners = [len(winners & numbers) for winners, numbers in sets]
per_card_copies = [1] * len(per_card_winners)
total = 0
for i, card in enumerate(per_card_winners):
    total += per_card_copies[i]
    if card >= 1:
        for j in range(i + 1, i + card + 1):
            per_card_copies[j] += per_card_copies[i]
print(total)"

echo
echo "test 2"
echo "$TEST" | python -c "$pysoln_bonus"

echo
echo "part 2"
cat $SCRIPT_DIR/input | python -c "$pysoln_bonus"
