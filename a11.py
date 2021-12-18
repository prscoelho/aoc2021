import numpy as np

example = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()

f = open("input/11.input")
text = f.read().strip()


def parse(t):
    res = []
    for line in t.split("\n"):
        for a in line:
            res.append(int(a))
    return np.reshape(np.array(res), (10, 10))


def in_bounds(row, col):
    return row >= 0 and row < 10 and col >= 0 and col < 10


def incr(matrix, row, col):
    matrix[max(0, row - 1):min(10, row + 2),
           max(0, col - 1):min(10, col + 2)] += 1


def step(matrix):
    result = matrix + 1
    n, m = np.shape(result)

    changed = True
    flashes = set()
    while changed:
        changed = False

        for i, j in np.argwhere(result > 9):
            flashes.add((i, j))
            incr(result, i, j)
            result[i][j] = -1000
            changed = True
    for row, col in flashes:
        result[row][col] = 0
    return result, len(flashes)


def part1(text):
    matrix = parse(text)
    flashes = 0
    for _ in range(100):
        matrix, flashes_occurred = step(matrix)
        flashes += flashes_occurred
    return flashes


def part2(text):
    matrix = parse(text)
    steps = 0
    while True:
        # if np.all(matrix == 0):
        #     break
        matrix, flashes = step(matrix)
        steps += 1
        if flashes == 100:
            break
    return steps


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
