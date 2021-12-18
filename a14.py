from collections import Counter

example = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip()

f = open("input/14.input")
text = f.read().strip()


def parse(t):
    start, rest = t.split("\n\n")

    rules = {}
    for line in rest.split("\n"):
        left, right = line.split(" -> ")
        rules[left] = right

    return start, rules


def grow(pairs, rules):
    result = Counter()
    for pair, frequency in pairs.items():
        left = pair[0] + rules[pair]
        right = rules[pair] + pair[1]
        result[left] += frequency
        result[right] += frequency
    return result


def get_pairs(polymer):
    pairs = Counter()
    for i in range(1, len(polymer)):
        pair = polymer[i-1:i+1]
        pairs[pair] += 1
    return pairs


def quantify(start, pairs):
    counter = Counter()
    counter[start[0]] += 1
    # ABCDE => AB BC CD DE => A: 1, B: 2, C: 2, D: 2, E: 1
    # every element except the leftmost and rightmost is repeated in every pair
    # we can get total letter count by counting the right element of each pair and the first element of start
    # since the leftmost element never changes during growth
    for pair, frequency in pairs.items():
        counter[pair[1]] += frequency
    commons = counter.most_common()
    return commons[0][1] - commons[-1][1]


def run(start, rules, iterations):
    pairs = get_pairs(start)
    for _ in range(iterations):
        pairs = grow(pairs, rules)
    return quantify(start, pairs)


def part1(text):
    start, rules = parse(text)
    return run(start, rules, 10)


def part2(text):
    start, rules = parse(text)
    return run(start, rules, 40)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
