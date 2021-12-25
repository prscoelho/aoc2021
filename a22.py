from functools import reduce


def flatMap(array):
    return reduce(list.__add__, array)


example = """
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""".strip()

example2 = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""".strip()

day_string = "22"
f = open(f"input/{day_string}.input")
text = f.read().strip()


def parse(t):
    result = []
    for line in t.split("\n"):
        state, rest = line.split()
        coords = []
        for coord in rest.split(","):
            nums = coord[2:].split("..")
            coords.append((int(nums[0]), int(nums[1]) + 1))
        result.append((state, coords))
    return result


def apply(cubes, action):
    ranges = action[1]
    x_range = ranges[0]
    x_range = (max(-50, x_range[0]), min(50, x_range[1]))
    y_range = ranges[1]
    y_range = (max(-50, y_range[0]), min(50, y_range[1]))
    z_range = ranges[2]
    z_range = (max(-50, z_range[0]), min(50, z_range[1]))

    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            for z in range(z_range[0], z_range[1]):
                tup = (x, y, z)
                if action[0] == 'on':
                    cubes.add(tup)
                else:
                    if tup in cubes:
                        cubes.remove(tup)


def area(cube):
    total = 1
    for i in range(3):
        total *= cube[i][1] - cube[i][0]
    return total


def range_intersection(a, b):
    return (a[0] <= b[1] and a[1] >= b[0]) or (b[0] <= a[1] and b[1] >= a[0])


def check_intersection(cube1, cube2):
    return all(range_intersection(a, b) for a, b in zip(cube1, cube2))


def contains(cube1, cube2):
    return cube1[0][0] <= cube2[0][0] and cube1[0][1] >= cube2[0][1] and cube1[1][0] <= cube2[1][0] and cube1[1][1] >= cube2[1][1] and cube1[2][0] <= cube2[2][0] and cube1[2][1] >= cube2[2][1]


def cuboid_subtraction(cube1, cube2):
    if contains(cube2, cube1):
        return []

    if not check_intersection(cube1, cube2):
        return [cube1]

    xmiddle = filter(lambda x: cube1[0][0] < x < cube1[0][1], cube2[0])
    ymiddle = filter(lambda y: cube1[1][0] < y < cube1[1][1], cube2[1])
    zmiddle = filter(lambda z: cube1[2][0] < z < cube1[2][1], cube2[2])

    result = []

    xv = [cube1[0][0]] + list(xmiddle) + [cube1[0][1]]
    yv = [cube1[1][0]] + list(ymiddle) + [cube1[1][1]]
    zv = [cube1[2][0]] + list(zmiddle) + [cube1[2][1]]

    for i in range(len(xv) - 1):
        for j in range(len(yv) - 1):
            for k in range(len(zv) - 1):
                new_cube = []
                new_cube.append((xv[i], xv[i + 1]))
                new_cube.append((yv[j], yv[j + 1]))
                new_cube.append((zv[k], zv[k + 1]))

                result.append(new_cube)

    return filter(lambda c: not contains(cube2, c), result)


def part1(text):
    actions = parse(text)
    cubes = set()
    for action in actions:
        apply(cubes, action)
    return len(cubes)


def part2(text):
    actions = parse(text)
    cubes = []
    for state, cube2 in actions:
        next_cubes = []
        for cube1 in cubes:
            next_cubes.extend(cuboid_subtraction(cube1, cube2))
        cubes = next_cubes
        if state == "on":
            cubes.append(cube2)
    return sum([area(cube) for cube in cubes])


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
