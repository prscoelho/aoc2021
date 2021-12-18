example = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

f = open("input/05.input")
text = f.read().strip()


def parse(t):
    res = []
    for line in t.split("\n"):
        left, right = line.split(" -> ")
        left = [int(n) for n in left.split(',')]

        right = [int(n) for n in right.split(',')]
        res.append((left, right))
    return res


def part1(text):
    parsed = parse(text)
    overlap = set()
    seen = set()

    for line in parsed:
        x1, y1 = line[0]
        x2, y2 = line[1]

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x1, y) in seen:
                    overlap.add((x1, y))
                seen.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if (x, y1) in seen:
                    overlap.add((x, y1))
                seen.add((x, y1))

    return len(overlap)


def part2(text):
    parsed = parse(text)
    overlap = set()
    seen = set()

    for line in parsed:
        x1, y1 = line[0]
        x2, y2 = line[1]

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x1, y) in seen:
                    overlap.add((x1, y))
                seen.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if (x, y1) in seen:
                    overlap.add((x, y1))
                seen.add((x, y1))
        else:
            if x1 > x2:
                tmp = x2, y2
                x2, y2 = x1, y1
                x1, y1 = tmp
            dy = 1 if y1 < y2 else -1
            y = y1
            for x in range(x1, x2 + 1):
                if (x, y) in seen:
                    overlap.add((x, y))
                seen.add((x, y))
                y += dy

    return len(overlap)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


main(example)
print()
main(text)
