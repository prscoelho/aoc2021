example = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()

f = open("input/12.input")
text = f.read().strip()


def parse(t):
    graph = {}
    for line in t.split("\n"):
        left, right = line.split('-')
        if left not in graph:
            graph[left] = set()
        if right not in graph:
            graph[right] = set()
        graph[left].add(right)
        graph[right].add(left)
    return graph


def paths(graph):
    queue = [("start", set(["start"]))]
    ended = 0
    while len(queue) > 0:
        position, visited = queue.pop()

        if position == "end":
            ended += 1
        else:
            for neighbour in graph[position]:
                didnt_visit = neighbour not in visited
                allowed = neighbour[0].isupper() or didnt_visit

                if allowed:
                    next_visited = visited.copy()
                    next_visited.add(neighbour)
                    queue.append((neighbour, next_visited))
    return ended


def paths_special(graph):
    queue = [("start", set(["start"]), False)]
    ended = 0
    while len(queue) > 0:
        position, visited, walked_twice = queue.pop()

        if position == "end":
            ended += 1
        else:
            for neighbour in graph[position]:
                didnt_visit = neighbour not in visited
                allowed = neighbour[0].isupper() or didnt_visit
                allowed_special = not walked_twice and neighbour != "start"

                if allowed or allowed_special:
                    next_walked_twice = walked_twice or not allowed
                    next_visited = visited.copy()
                    next_visited.add(neighbour)
                    queue.append((neighbour, next_visited,
                                 next_walked_twice))
    return ended


def part1(text):
    parsed = parse(text)
    return paths(parsed)


def part2(text):
    parsed = parse(text)
    return paths_special(parsed)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
