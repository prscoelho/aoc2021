day_string = "24"
f = open(f"input/{day_string}.input")
text = f.read().strip()


def parse(text):
    lines = [line.split() for line in text.split('\n')]
    res = []
    for i in range(14):
        idx = 18 * i
        a = int(lines[idx + 4][2])
        b = int(lines[idx + 5][2])
        c = int(lines[idx + 15][2])
        res.append((a, b, c))
    return res


abc = parse(text)


def one_segment(w, z, a, b, c):
    x = int((z % 26) + b != w)
    z //= a
    z *= 25*x+1
    z += (w+c)*x
    return z


def alu(abc, input):
    x, z = 0, 0
    for i in range(14):
        a, b, c = abc[i]
        w = int(input[i])
        z = one_segment(w, z, a, b, c)
    return z


def build_pairs(abc):
    stack = []
    res = dict()
    for i in range(14):
        if abc[i][0] == 26:
            prev_i = stack.pop()
            prev_c = abc[prev_i][2]

            current_b = abc[i][1]
            diff = prev_c + current_b
            res[(prev_i, i)] = diff
        else:
            stack.append(i)
    return res


g = build_pairs(abc)


def optimize(g, fn):
    res = [0] * 14
    for (i, j) in g:
        diff = g[(i, j)]
        ival = fn(n for n in range(1, 10) if 0 < n + diff < 10)
        jval = ival + diff

        res[i] = ival
        res[j] = jval
    return "".join(str(n) for n in res)


part1 = optimize(g, max)
assert alu(abc, part1) == 0

part2 = optimize(g, min)
assert alu(abc, part2) == 0

print("Part 1:", part1)
print("Part 2:", part2)
