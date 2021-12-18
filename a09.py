example = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip()

f = open("input/09.input")
text = f.read().strip()


def parse(t):
    return [[int(a) for a in line] for line in t.split("\n")]


def valid(x, y, cols, rows):
    return x >= 0 and x < cols and y >= 0 and y < rows


def is_low_point(parsed, x, y):
    rows = len(parsed)
    cols = len(parsed[0])

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == dx == 0:
                continue
            pos_y = y + dy
            pos_x = x + dx
            if valid(pos_x, pos_y, cols, rows) and parsed[pos_y][pos_x] <= parsed[y][x]:
                return False
    return True


def part1(text):
    parsed = parse(text)
    rows = len(parsed)
    cols = len(parsed[0])
    lows = []
    for y in range(rows):
        for x in range(cols):
            if is_low_point(parsed, x, y):
                lows.append((x, y))
    return len(lows) + sum(map(lambda xy: parsed[xy[1]][xy[0]], lows))


def find_basin(parsed, start):
    rows = len(parsed)
    cols = len(parsed[0])

    visited = set([start])
    queue = [start]

    while len(queue) > 0:
        x, y = queue.pop()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos_y = y + dy
            pos_x = x + dx
            if valid(pos_x, pos_y, cols, rows) and parsed[pos_y][pos_x] < 9 and (pos_x, pos_y) not in visited:
                visited.add((pos_x, pos_y))
                queue.append((pos_x, pos_y))
    return visited


def part2(text):
    parsed = parse(text)
    visited = set()

    rows = len(parsed)
    cols = len(parsed[0])

    basins = []

    for y in range(rows):
        for x in range(cols):
            node = (x, y)
            if parsed[y][x] != 9 and node not in visited:
                basin = find_basin(parsed, node)
                visited |= basin
                basins.append(len(basin))
    basins.sort()
    return basins[-1] * basins[-2] * basins[-3]


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
