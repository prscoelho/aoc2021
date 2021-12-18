from a16 import parse as parse_packets, value

example = """
9C0141080250320F1802104A08
""".strip()

day_string = "00"
f = open(f"input/{day_string}.input")
text = f.read().strip()

# This is a template file in case a future exercise requires decoding packets


def parse(t):
    return parse_packets(t)


def part1(text):
    parsed = parse(text)
    print(parsed)


def part2(text):
    parsed = parse(text)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
main(example)
print("==== SOLUTION RESULT ====")
main(text)
