example = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip()

f = open("input/13.input")
text = f.read().strip()


def parse(t):
    dots_text, folds_text = t.split("\n\n")

    dots = set()
    for line in dots_text.split("\n"):
        x, y = [int(a) for a in line.split(",")]
        dots.add((x, y))
    folds = []
    for line in folds_text.split("\n"):
        equation = line.split()[2]
        axis, value = equation.split("=")
        folds.append((axis, int(value)))
    return dots, folds


def fold_paper(paper, at):
    result = set()
    if at[0] == "x":
        for coord in paper:
            if coord[0] < at[1]:
                result.add(coord)
            else:
                new_coord = (at[1] * 2 - coord[0], coord[1])
                result.add(new_coord)
    else:
        for coord in paper:
            if coord[1] < at[1]:
                result.add(coord)
            else:
                new_coord = (coord[0], at[1] * 2 - coord[1])
                result.add(new_coord)
    return result


def part1(text):
    paper, folds = parse(text)

    paper = fold_paper(paper, folds[0])
    return len(paper)


def display_paper(paper):
    total_y = max([coord[1] for coord in paper])
    total_x = max([coord[0] for coord in paper])

    res = "\n"

    for y in range(total_y + 1):
        for x in range(total_x + 1):
            if (x, y) in paper:
                res += '█'
            else:
                res += " "
        res += "\n"
    return res


def part2(text):
    paper, folds = parse(text)

    for fold_equation in folds:
        paper = fold_paper(paper, fold_equation)
    return display_paper(paper)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
