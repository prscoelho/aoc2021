from functools import reduce
from operator import and_

example = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip()

f = open("input/08.input")
text = f.read().strip()


def parse(t):
    return [[[set(part) for part in parts.split(" ")] for parts in line.split(" | ")] for line in t.split("\n")]


def part1(text):
    entries = parse(text)
    count = 0
    sizes = [2, 3, 4, 7]
    for _, right in entries:
        for segment in right:
            s = len(segment)
            if s in sizes:
                count += 1
    return count


def decode(entry):
    left, right = entry
    by_size = {s: [] for s in [2, 3, 4, 5, 6, 7]}
    for segment in left:
        size = len(segment)
        by_size[size].append(segment)

    # 1 => 2 =>   c  f
    # 7 => 3 => a c  f
    # 4 => 4 =>  bcd f
    # 2 => 5 => a cde g
    # 3 => 5 => abcd fg
    # 5 => 5 => ab d fg
    # 0 => 6 => abc efg
    # 6 => 6 => ab defg
    # 9 => 6 => abcd fg
    # 8 => 7 => abcdefg

    cf = by_size[2][0]      # only number 1 contains 2 segments
    bcdf = by_size[4][0]    # only number 4 contains 4 segments
    acf = by_size[3][0]     # only number 7 contains 3 segments
    abcdefg = by_size[7][0]  # only number 8 contains 7 segments

    a = acf - cf

    aeg = abcdefg - bcdf
    eg = aeg - a

    adg = reduce(and_, by_size[5])
    abfg = reduce(and_, by_size[6])

    e = eg - adg
    g = eg - e
    d = adg - a - g
    b = bcdf - cf - d
    c = cf - abfg
    f = cf - c

    translation = {s.pop(): ch
                   for s, ch in zip([a, b, c, d, e, f, g], "abcdefg")}

    return sum([display_number(segment, translation) * 10 ** idx for idx, segment in enumerate(reversed(right))])


def convert(word, mapping):
    """Converts a segment from jumbled to display wires"""
    res = set()
    for w in word:
        res.add(mapping[w])
    return res


displays = {0: set("abcefg"),
            1: set("cf"),
            2: set("acdeg"),
            3: set("acdfg"),
            4: set("bcdf"),
            5: set("abdfg"),
            6: set("abdefg"),
            7: set("acf"),
            8: set("abcdefg"),
            9: set("abcdfg")
            }


def display_number(word, translation):
    """Converts a segment from jumbled to display wires, and returns the displayed number"""
    converted = convert(word, translation)
    for number, wires in displays.items():
        if wires == converted:
            return number


def part2(text):
    entries = parse(text)
    return sum([decode(entry) for entry in entries])


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


print("==== EXAMPLES ====")
example_parsed = parse(
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
print(decode(example_parsed[
      0]), "== 5353")
main(example)
print("==== SOLUTION RESULT ====")
main(text)


# initial solution, creates mappings based on 1, 4, 7 and 8, with most letters having two possibilities
# and trying each possible combination, stopping when one combination generates all valid numbers

def assume(mapping, a, b):
    """assume that a -> b and return the resulting mapping"""
    res = {k: v.copy() for k, v in mapping.items()}
    res[a] = set(b)
    for k, v in res.items():
        if b in v and k != a:
            v.remove(b)
    return res


def possible_mappings(mapping):
    if all([len(v) == 1 for v in mapping.values()]):
        yield mapping
    if not any([len(v) == 0 for v in mapping.values()]):
        res = []
        for k, v in mapping.items():
            if len(v) > 1:
                for a in v:
                    for p in possible_mappings(assume(mapping, k, a)):
                        yield p
                break


def convert_dict(word, mapping):
    res = set()
    for w in word:
        res.add(list(mapping[w])[0])
    return res


def as_string(word):
    res_list = []
    for a in word:
        res_list.append(a)
    return "".join(sorted(res_list))


def check_mappings(words, mapping):
    """checks if mapping is valid and returns a dict of [word] = num"""
    translation = dict()
    for word in words:
        converted = convert_dict(word, mapping)
        matching = [k for k, v in displays.items() if v == converted]

        if len(matching) != 1:
            return None
        else:
            num = matching[0]
            translation[frozenset(word)] = num
    return translation


all_on = set("abcdefg")


def translate_old(t, right):
    return sum([t[frozenset(word)] * 10**idx for idx, word in enumerate(reversed(right))])


def decode_old(entry):
    # map from segment to real wire
    mapping = {c: set("abcdefg") for c in "abcdefg"}
    left, right = entry
    for segment in left + right:
        s = len(segment)
        if s in sizes:
            difference = all_on - segment
            num = sizes[s]
            for c in segment:
                mapping[c] &= displays[num]
            for d in difference:
                mapping[d] -= displays[num]
    for possible in possible_mappings(mapping):
        t = check_mappings(left, possible)
        if t is not None:
            return translate_old(t, right)
