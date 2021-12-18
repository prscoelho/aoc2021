from heapq import heappush, heappop

example = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()

f = open("input/15.input")
text = f.read().strip()


def parse(t):
    return [[int(a) for a in line] for line in t.split("\n")]


def valid(pos, rows, cols):
    return pos[0] >= 0 and pos[0] < rows and pos[1] >= 0 and pos[1] < cols


def dijkstra(matrix, start, goal):
    heap = [(0, start)]

    rows = len(matrix)
    cols = len(matrix[0])

    visited = {start: 0}

    while len(heap) > 0:
        cost, position = heappop(heap)

        if position == goal:
            return cost

        if visited[position] < cost:
            continue

        for change in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbour = position[0] + change[0], position[1] + change[1]

            if valid(neighbour, rows, cols):
                next_cost = cost + matrix[neighbour[0]][neighbour[1]]
                if visited.get(neighbour, 1e10) <= next_cost:
                    continue
                visited[neighbour] = next_cost
                heappush(heap, (next_cost, neighbour))


def part1(text):
    parsed = parse(text)
    return dijkstra(parsed, (0, 0), (len(parsed) - 1, len(parsed[0]) - 1))


def expand_map(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    result = [[0 for _ in range(cols * 5)] for _ in range(rows * 5)]

    for i in range(5):
        for j in range(5):
            for y in range(rows):
                for x in range(cols):
                    value = matrix[y][x] + i + j
                    value = value % 10 + (1 if value >= 10 else 0)
                    result[y + rows * i][x + cols * j] = value
    return result


def part2(text):
    parsed = parse(text)
    expanded = expand_map(parsed)
    goal = (len(expanded) - 1, len(expanded[0]) - 1)
    return dijkstra(expanded, (0, 0), goal)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
