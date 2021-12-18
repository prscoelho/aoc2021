from functools import reduce

example = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()

f = open("input/10.input")
text = f.read().strip()


def parse(t):
    return t.split("\n")


opening = ['(', "[", '<', '{']
closing = [')', "]", '>', '}']
scores_corrupted = {')': 3, ']': 57, '}': 1197, '>': 25137}
scores_complete = {'(': 1, '[': 2, '{': 3, '<': 4}


def corrupted_char(line):
    found = []
    for c in line:
        if c in opening:
            found.append(c)
        elif c in closing:
            last_opened = found.pop()
            idx_open = opening.index(last_opened)
            idx_close = closing.index(c)
            if idx_open != idx_close:
                return c, None
    return None, found


def part1(text):
    parsed = parse(text)
    return sum(
        map(scores_corrupted.get,
            filter(lambda c: c is not None,
                   map(lambda line: corrupted_char(line)[0], parsed))))


def complete_score(remaining):
    return reduce(lambda acc, opened: acc * 5 + scores_complete[opened], reversed(remaining), 0)


def part2(text):
    parsed = parse(text)
    scores = sorted(
        map(complete_score,
            filter(lambda l: l is not None,
                   map(lambda line: corrupted_char(line)[1], parsed)))
    )
    return scores[len(scores) // 2]


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
