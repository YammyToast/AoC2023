"""
--- Day 5: If You Give A Seed A Fertilizer ---
"""


import re
import random


EXAMPLES1 = (("input.txt", 35),)

EXAMPLES2 = (("input.txt", 46),)

INPUT = "input.txt"


PATTERN = """\
seeds: ([0-9 ]+)

seed-to-soil map:
([0-9 \n]+)

soil-to-fertilizer map:
([0-9 \n]+)

fertilizer-to-water map:
([0-9 \n]+)

water-to-light map:
([0-9 \n]+)

light-to-temperature map:
([0-9 \n]+)

temperature-to-humidity map:
([0-9 \n]+)

humidity-to-location map:
([0-9 \n]+)
"""


def read_data(filename):
    with open(filename) as f:
        data = f.read()
    match = re.match(PATTERN, data)
    seeds = [int(_) for _ in re.findall(r"\d+", match.group(1))]
    maps = [None] * 7
    for k in range(7):
        lines = match.group(k + 2).splitlines()
        maps[k] = [[int(_) for _ in re.findall(r"\d+", line)] for line in lines]
    return seeds, maps


def follow_map(map_, val):
    for dest, source, range_ in map_:
        if source <= val < source + range_:
            return dest + val - source
    else:
        return val


def follow_maps(maps, val):
    for map_ in maps:
        val = follow_map(map_, val)
    return val


def reverse_map(map_, val):
    for dest, source, range_ in map_:
        if dest <= val < dest + range_:
            return source + val - dest
    else:
        return val


def compose_2maps(map1, map2):
    bornes = set([0])
    for dest, source, range_ in map1:
        bornes.add(source)
        bornes.add(source + range_)
    for dest, source, range_ in map2:
        bornes.add(reverse_map(map1, source))
        bornes.add(reverse_map(map1, source + range_))
    bornes = sorted(bornes)

    maps = [map1, map2]
    newmap = []
    for v1, v2 in zip(bornes[:-1], bornes[1:]):
        w1 = follow_maps(maps, v1)
        newmap.append((w1, v1, v2 - v1))

    return newmap


def compose_maps(maps):
    map1 = maps[0]
    for map2 in maps[1:]:
        map1 = compose_2maps(map1, map2)
    return map1


def test_compose(maps):
    newmap = compose_maps(maps)
    for _ in range(100_000):
        p = random.randrange(2731269124)
        q1 = follow_maps(maps, p)
        q2 = follow_map(newmap, p)
        assert q1 == q2


def code1(data):
    seeds, maps = data
    return min(follow_maps(maps, seed) for seed in seeds)


def code2_naif(data):
    seeds, maps = data
    minval = float("inf")
    for start, length in zip(seeds[::2], seeds[1::2]):
        for seed in range(start, start + length):
            minval = min(minval, follow_maps(maps, seed))
    return minval


def code2(data):
    seeds, maps = data
    map_ = compose_maps(maps)
    minval = float("inf")
    for start, length in zip(seeds[::2], seeds[1::2]):
        for dest, source, range_ in map_:
            if start <= source < start + length:
                minval = min(minval, follow_map(map_, source))
            elif source < start and source + range_ - 1 < start + length:
                minval = min(minval, follow_map(map_, start))
    return minval


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        # assert expected is None or result == expected, (data, expected, result)

    print(f"{n}>", code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
