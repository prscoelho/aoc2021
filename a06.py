example = """3,4,3,1,2"""

f = open("input/06.input")
text = f.read().strip()


def parse(t):
    fish_timers = [int(a) for a in t.split(",")]
    fish = [0] * 9
    for timer in fish_timers:
        fish[timer] += 1
    return fish


def part1(text):
    fish = parse(text)
    for _ in range(80):
        fish = tick(fish)
    return sum(fish)


def tick(fish):
    result = [0] * 9

    result[8] = fish[0]
    for idx in range(1, len(fish)):
        result[idx - 1] += fish[idx]
    result[6] += fish[0]
    return result


def part2(text):
    fish = parse(text)

    for _ in range(256):
        fish = tick(fish)
    return sum(fish)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


main(example)
print()
main(text)
