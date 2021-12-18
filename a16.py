from operator import mul
from functools import reduce
from collections import namedtuple

f = open("input/16.input")
text = f.read().strip()

Packet = namedtuple("Packet", ["version", "type", "content"])


def parse_literal(t):
    literal = 0
    found_zero = False
    while not found_zero:
        if t[0] == '0':
            # last number
            found_zero = True
        value, t = int(t[1:5], 2), t[5:]
        literal = (literal << 4) + value
    return literal, t


def parse_operator(t):
    packets = []
    if t[0] == '0':
        total_bit_length, t = int(t[1:16], 2), t[16:]
        to_read, t = t[:total_bit_length], t[total_bit_length:]
        while len(to_read) > 0:
            packet, to_read = parse_packet(to_read)
            packets.append(packet)
    else:
        packets_count, t = int(t[1:12], 2), t[12:]
        for _ in range(packets_count):
            packet, t = parse_packet(t)
            packets.append(packet)
    return packets, t


def parse_packet(t):
    version, t = int(t[:3], 2), t[3:]
    type_id, t = int(t[:3], 2), t[3:]

    if type_id == 4:
        literal, t = parse_literal(t)
        return Packet(version, type_id, literal), t
    else:
        operator, t = parse_operator(t)
        return Packet(version, type_id, operator), t


def parse(t):
    as_binary = "".join(["{0:04b}".format(int(a, 16)) for a in t])
    return parse_packet(as_binary)[0]


def count_version(packet):
    total = packet.version
    if packet[1] != 4:
        for p in packet[2]:
            total += count_version(p)
    return total


def part1(text):
    parsed = parse(text)
    return count_version(parsed)


def value(packet):
    type_id = packet.type
    if type_id == 4:
        return packet.content
    else:
        values = [value(p) for p in packet.content]
        if type_id == 0:
            return sum(values)
        elif type_id == 1:
            return reduce(mul, values, 1)
        elif type_id == 2:
            return min(values)
        elif type_id == 3:
            return max(values)
        elif type_id == 5:
            return int(values[0] > values[1])
        elif type_id == 6:
            return int(values[0] < values[1])
        elif type_id == 7:
            return int(values[0] == values[1])


def part2(text):
    parsed = parse(text)
    return value(parsed)


def main(text):
    print("Part1:", part1(text))
    print("Part2:", part2(text))


if __name__ == "__main__":
    print("==== EXAMPLES ====")
    print(parse_packet("110100101111111000101000")[0][2], "should be 2021")
    print(parse_packet("00111000000000000110111101000101001010010001001000000000")[0],
          "should contain two packets with values 10 and 20")
    print(parse_packet("11101110000000001101010000001100100000100011000001100000")[0],
          "should contain three packets with values 1, 2, 3")
    print("Part1:", part1("A0016C880162017C3686B18A3D4780"), "should be 31")
    print("Part2:", part2("9C0141080250320F1802104A08"), "should be 1")
    print("==== SOLUTION RESULT ====")
    main(text)
