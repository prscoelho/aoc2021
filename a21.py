from itertools import combinations_with_replacement, permutations
from collections import Counter
start_example = [4, 8]

start = [4, 5]


def calc_position(total):
    while total > 10:
        rem = total % 11
        to_add = total // 11
        total = rem + to_add
    return total


def calc_rolls(die):
    value = 0
    for _ in range(3):
        value += die
        die += 1
        if die == 101:
            die = 1
    return value, die


dice_throw_permutations = []
for comb in combinations_with_replacement([1, 2, 3], 3):
    dice_throw_permutations.extend(set(permutations(comb)))
universe_rolls = Counter([sum(l) for l in dice_throw_permutations])


def part1(starts):
    players = starts.copy()

    scores = [0, 0]

    die = 1
    die_rolls = 0

    while True:
        for i in range(2):
            if scores[(i + 1) % 2] >= 1000:
                return scores[i] * die_rolls
            rolls, die = calc_rolls(die)
            die_rolls += 3

            new_pos = calc_position(players[i] + rolls)
            scores[i] += new_pos
            players[i] = new_pos


def part2(starts):
    positions = tuple(starts)
    scores = (0, 0)

    universe_scores = [0, 0]

    states = Counter()
    states[(positions, scores, 0)] = 1

    while len(states) > 0:
        k, num_states = next(iter(states.items()))
        positions, scores, player = k
        for rolls, states_created in universe_rolls.items():
            new_pos = calc_position(positions[player] + rolls)
            new_score = scores[player] + new_pos
            total_states = states_created * num_states
            if new_score >= 21:
                universe_scores[player] += total_states
            else:
                new_positions = tuple(
                    positions[j] if j != player else new_pos for j in range(2))
                new_scores = tuple(
                    scores[j] if j != player else new_score for j in range(2))
                next_player = (player + 1) % 2
                states[(new_positions, new_scores, next_player)] += total_states
        del states[k]
    return max(universe_scores)


def main(start):
    print("Part1:", part1(start))
    print("Part2:", part2(start))


print("==== EXAMPLES ====")
main(start_example)
print("==== SOLUTION RESULT ====")
main(start)
