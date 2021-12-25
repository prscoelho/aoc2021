example = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()

day_string = "20"
f = open(f"input/{day_string}.input")
text = f.read().strip()


def parse(t):
    algorithm, rest = t.split("\n\n")

    image = dict()
    for row, line in enumerate(rest.split("\n")):
        for col, c in enumerate(line):
            cell = True if c == "#" else False
            image[row, col] = cell
    return algorithm, image


def neighbours(row, col):
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            yield drow + row, dcol + col


def bin_number(image, row, col, void):
    result = ""
    for r, c in neighbours(row, col):
        if image.get((r, c), void):
            result += '1'
        else:
            result += "0"
    return int(result, 2)


def step(image, algorithm, void):
    result = dict()

    low_row = min(row for row, _ in image.keys()) - 1
    low_col = min(col for _, col in image.keys()) - 1

    high_row = max(row for row, _ in image.keys()) + 1
    high_col = max(col for _, col in image.keys()) + 1

    for row in range(low_row, high_row + 1):
        for col in range(low_col, high_col + 1):
            n = bin_number(image, row, col, void)
            cell = True if algorithm[n] == '#' else False
            result[row, col] = cell
    return result


def run(algo, image, iters):
    void = False
    for i in range(iters):
        image = step(image, algo, void)
        if algo[0] == "#":
            if i % 2 == 0:
                void = True
            else:
                void = algo[-1] == "#"
    return image


def part1(text):
    algo, image = parse(text)
    image = run(algo, image, 2)
    return sum(image.values())


def part2(text):
    algo, image = parse(text)
    image = run(algo, image, 50)
    return sum(image.values())


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
