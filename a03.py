example = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

f = open("input/03.input")
text = f.read()

def parse(t):
    return[[int(b) for b in line] for line in t.strip().split('\n')]
def to_dec(a):
    return sum([b * (2 ** n) for (n, b) in enumerate(reversed(a))])
# splits elements into [zero_at_col, one_at_col]
def split_by_col(matrix, col):
    return [[element for element in matrix if element[col] == bit] for bit in [0, 1]]
def part1(text):
    parsed = parse(text)
    gamma = 0
    col_size = len(parsed[0])
    for col in range(col_size):
        containing_zero, containing_one = split_by_col(parsed, col)
        zeros, ones = len(containing_zero), len(containing_one)
        if ones > zeros:
            p = col_size - 1 - col
            gamma += 2 ** p
    all_ones = 2 ** col_size - 1
    epsilon = ~gamma & all_ones
    return gamma * epsilon
def calculate_rating(matrix, rules):
    # rules[idx] = what bit to keep if idx is most common
    # [0, 1] => keep 0 if 0 is most common, keep 1 if 1 is most common
    # [1, 0] => keep 1 if 0 is most common, keep 0 if 1 is most common
    for col in range(len(matrix[0])):
        if len(matrix) == 1:
            break
        containing = split_by_col(matrix, col)
        if len(containing[1]) >= len(containing[0]):
            matrix = containing[rules[1]]
        else:
            matrix = containing[rules[0]]
    return to_dec(matrix[0])
def part2(text):
    parsed = parse(text)
    oxygen = calculate_rating(parsed, [0, 1])
    co = calculate_rating(parsed, [1, 0])
    return oxygen * co
def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))
main(example)
print()
main(text)
