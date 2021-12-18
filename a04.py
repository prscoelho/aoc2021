example = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

f = open("input/04.input")
text = f.read().strip()


def parse(t):
    tokens = t.split('\n\n')
    upper = tokens[0]
    rest = tokens[1:]

    numbers = [int(number) for number in upper.split(",")]
    grids = [[int(number) for number in grid.split()] for grid in rest]
    return numbers, grids


def score(grid, marked_indexes, last_number):
    return last_number * sum([grid[idx] for idx in range(len(grid)) if idx not in marked_indexes])


def check_completed(marked_indexes):
    # check cols
    for col in range(5):
        if all([row * 5 + col in marked_indexes for row in range(5)]):
            return True
    # check rows
    for row in range(5):
        if all([row * 5 + col in marked_indexes for col in range(5)]):
            return True
    return False


def part1(text):
    numbers, grids = parse(text)
    marked_indexes = [set() for _ in range(len(grids))]

    for number in numbers:
        for (grid_index, grid) in enumerate(grids):
            if number in grid:
                idx = grid.index(number)
                marked_indexes[grid_index].add(idx)
                if check_completed(marked_indexes[grid_index]):
                    return score(grid, marked_indexes[grid_index], number)


def part2(text):
    numbers, grids = parse(text)
    marked_indexes = [set() for _ in range(len(grids))]
    completed = set()

    for number in numbers:
        for (grid_index, grid) in enumerate(grids):
            if grid_index not in completed and number in grid:
                idx = grid.index(number)
                marked_indexes[grid_index].add(idx)
                if check_completed(marked_indexes[grid_index]):
                    completed.add(grid_index)
                    if len(completed) == len(grids):
                        return score(grid, marked_indexes[grid_index], number)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


main(example)
print()
main(text)
