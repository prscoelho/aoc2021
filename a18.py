from functools import reduce
from collections import namedtuple

example = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".strip()

day_string = "18"
f = open(f"input/{day_string}.input")
text = f.read().strip()

Element = namedtuple("Element", ["value", "depth"])


def parse_pair(t):
    depth = 0
    pair = []
    for a in t:
        if a == "[":
            depth += 1
        elif a == "]":
            depth -= 1
        elif a.isdigit():
            element = Element(int(a), depth)
            pair.append(element)
    if depth != 0:
        print("Unexpected end of depth:", depth)
    return pair


def parse(t):
    return [parse_pair(line) for line in t.split("\n")]


def add_element(e1, e2):
    return Element(e1.value + e2.value, e1.depth)


def increase_depth(element):
    return Element(element.value, element.depth + 1)


def explode(snailfish):
    for idx in range(1, len(snailfish)):
        right = snailfish[idx]
        left = snailfish[idx - 1]

        if left.depth == right.depth == 5:
            if idx - 2 >= 0:
                snailfish[idx - 2] = add_element(snailfish[idx - 2], left)
            if idx + 1 < len(snailfish):
                snailfish[idx + 1] = add_element(snailfish[idx + 1], right)
            snailfish[idx - 1] = Element(0, right.depth - 1)
            del snailfish[idx]
            return True
    return False


def split_snailfish(snailfish):
    for idx in range(len(snailfish)):
        if snailfish[idx].value > 9:
            value = snailfish[idx].value
            new_depth = snailfish[idx].depth + 1
            snailfish[idx] = Element(value // 2, new_depth)
            new_element = Element(value // 2 + (1 if value %
                                  2 == 1 else 0), new_depth)
            snailfish.insert(idx + 1, new_element)
            return True
    return False


def reduce_snailfish(snailfish):
    while True:
        if not (explode(snailfish) or split_snailfish(snailfish)):
            break
    return snailfish


def addition(left, right):
    added = [increase_depth(element) for element in left + right]
    return reduce_snailfish(added)


def magnitude(snailfish):
    snailfish = snailfish.copy()
    # reduce snailfish until there's only one element left
    # we can reduce same depth pairs (left_num, right_num)
    #  into depth -1, 3 * left_value + 2 * right_value
    while len(snailfish) > 1:
        for i in range(1, len(snailfish)):
            left = snailfish[i - 1]
            right = snailfish[i]

            if left.depth == right.depth:
                combined = left.value * 3 + right.value * 2
                snailfish[i - 1] = Element(combined, left.depth - 1)
                del snailfish[i]
                break
    return snailfish[0].value


def part1(text):
    parsed = parse(text)
    total = reduce(addition,
                   parsed[1:], parsed[0])
    return magnitude(total)


def part2(text):
    parsed = parse(text)
    best = float('-inf')
    for i in range(len(parsed)):
        for j in range(len(parsed)):
            if i == j:
                continue
            mag = magnitude(addition(parsed[i], parsed[j]))
            best = max(best, mag)
    return best


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")


def test_magnitude(t, expected):
    parsed = parse_pair(t)
    assert magnitude(parsed) == expected


test_magnitude("[[1,2],[[3,4],5]]", 143)
test_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137)
test_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)


def test_explosion(t, expected_t):
    parsed = parse_pair(t)
    expected = parse_pair(expected_t)
    explode(parsed)
    assert parsed == expected


test_explosion("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]",
               "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

main(example)
print("==== SOLUTION RESULT ====")
main(text)
