f = open("input/02.input")
example = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
text = f.read()

def parse(t):
    res = []
    for line in t.strip().split('\n'):
        move, num = line.strip().split()
        num = int(num)
        res.append((move, num))
    return res

def part1(text):
    moves = parse(text)
    pos = 0
    depth = 0
    for (move, num) in moves:
        if move == "forward":
            pos += num
        elif move == "down":
            depth += num
        elif move == "up":
            depth -= num
        else:
            print("UNEXPECTED", move)
            return
    return pos * depth

def part2(text):
    moves = parse(text)
    pos = 0
    depth = 0
    aim = 0
    for (move, num) in moves:
        if move == "forward":
            pos += num
            depth += aim * num
        elif move == "down":
            aim += num
        elif move == "up":
            aim -= num
        else:
            print("UNEXPECTED", move)
            return
    return depth * pos

def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))
main(example)
print()
main(text)
