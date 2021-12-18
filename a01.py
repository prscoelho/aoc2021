f = open("input/01.input")
example = """199
200
208
210
200
207
240
269
260
263
"""
text = f.read()

def count_increases(nums, window=1):
    res = 0
    for idx in range(window, len(nums)):
        if sum(nums[idx-window:idx]) < sum(nums[idx-window+1:idx+1]):
            res += 1
    return res

def windows(nums):
    res = 0
    for i in range(3, len(nums)):
        left = nums[i - 3]
        right = nums[i]
        if left < right:
            res += 1
    return res
def part1(text):
    nums = [int(a.strip()) for a in text.strip().split("\n")]
    return count_increases(nums, 1)
def part2(text):
    nums = [int(a.strip()) for a in text.strip().split("\n")]
    #return count_increases(nums, 3)
    return windows(nums)
def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))
main(example)
print()
main(text)
