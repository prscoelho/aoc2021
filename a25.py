example = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()

day_string = "25"
f = open(f"input/{day_string}.input")
text = f.read().strip()


def parse(t):
    grid = t.split("\n")
    rows = len(grid)
    cols = len(grid[0])

    east = set()
    south = set()

    for row in range(rows):
        for col in range(cols):
            c = grid[row][col]
            if c == 'v':
                south.add((row, col))
            elif c == '>':
                east.add((row, col))

    return (rows, cols), east, south


def step(size, east, south):
    result_east = set()
    result_south = set()

    for (row, col) in east:
        next_pos = (row, (col + 1) % size[1])
        if next_pos not in east and next_pos not in south:
            result_east.add(next_pos)
        else:
            result_east.add((row, col))
    for (row, col) in south:
        next_pos = ((row + 1) % size[0], col)
        if next_pos not in south and next_pos not in result_east:
            result_south.add(next_pos)
        else:
            result_south.add((row, col))

    return result_east, result_south


def part1(text):
    size, east, south = parse(text)
    i = 1
    while True:
        next_east, next_south = step(size, east, south)
        if next_east == east and next_south == south:
            break
        east = next_east
        south = next_south
        i += 1
    return i


def main(text):
    print("Part1:", part1(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
