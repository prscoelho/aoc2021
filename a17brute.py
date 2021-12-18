example = """
target area: x=20..30, y=-10..-5
""".strip()


day_string = "17"
f = open(f"input/{day_string}.input")
text = f.read().strip()


def parse_range(t):
    t = t[2:]
    return [int(a) for a in t.split("..")]


def parse(t):
    _, coords = t.split(": ")
    x_range, y_range = coords.split(", ")
    return parse_range(x_range), parse_range(y_range)


def inside_area(position, area):
    return position[0] >= area[0][0] and position[0] <= area[0][1] and position[1] >= area[1][0] and position[1] <= area[1][1]


def update_velocity(vx, vy):
    # Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
    # Due to gravity, the probe's y velocity decreases by 1.
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    vy -= 1
    return vx, vy


def can_reach(v0, area):
    x, y = 0, 0
    vx, vy = v0

    highest_y = 0
    reached = False
    # print("trying to reach:", area)
    while y >= area[1][0]:
        x += vx
        y += vy
        # print(x, y)
        highest_y = max(highest_y, y)
        vx, vy = update_velocity(vx, vy)
        if inside_area((x, y), area):
            reached = True
    return reached, highest_y


def part1(text):
    area = parse(text)
    result = 0
    for x in range(area[0][1] + 1):
        for y in range(area[1][0], 150):
            reached, highest_y = can_reach((x, y), area)
            if reached:
                result = max(highest_y, result)
    return result


def part2(text):
    area = parse(text)
    result = 0

    for x in range(area[0][1] + 1):
        for y in range(area[1][0], 150):
            reached, _ = can_reach((x, y), area)
            if reached:
                result += 1
    return result


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
