from math import floor, ceil

example = """
16,1,2,0,4,2,7,1,2,14
""".strip()

f = open("input/07.input")
text = f.read().strip()


def parse(t):
    return [int(a) for a in t.split(',')]


def nth_sum(n):
    return n * (n + 1) // 2


def cost(nums, val, fn=lambda x: x):
    total = 0
    for num in nums:
        total += fn(abs(num - val))
    return total


def part1(text):
    parsed = parse(text)
    return min([cost(parsed, v) for v in range(min(parsed), max(parsed) + 1)])


def part2(text):
    parsed = parse(text)
    return min([cost(parsed, v, nth_sum) for v in range(min(parsed), max(parsed) + 1)])


def mean(nums):
    return sum(nums) / len(nums)


def median(nums):
    return sorted(nums)[(len(nums) + 1) // 2]


def part1s(text):
    nums = parse(text)
    return cost(nums, median(nums))


def part2s(text):
    nums = parse(text)
    # the mean gives us an approximation of the minimum value for nth_sum, within -1/2 <= min_val <= +1/2
    approximation = mean(nums)
    return min(cost(nums, floor(approximation), nth_sum), cost(nums, ceil(approximation), nth_sum))


def main(text):
    print("Part1:", part1s(text))
    print("Part2:", part2s(text))


main(example)
print()
main(text)
