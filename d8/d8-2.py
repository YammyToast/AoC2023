import re
import numpy


def analyse_file(__filename: str):
    with open(__filename) as f:
        lines = f.readlines()
    instructions = list(lines[0].strip("\n"))
    raw_destinations = [c.strip("\n").split(" = ") for c in lines[2:]]
    destinations = {}
    for dest in raw_destinations:
        destinations[dest[0]] = tuple(re.sub("[() ]", "", dest[1]).split(","))

    starts = [c for c in destinations.keys() if re.match(r"([A-Z]{2}A)", c) != None]
    ends = [c for c in destinations.keys() if re.match(r"([A-Z]{2}Z)", c) != None]

    step_list = []
    for start in starts:
        loc = start
        steps = 0

        while loc not in ends:
            for instruction in instructions:
                if loc in ends:
                    break
                loc = destinations[loc][instruction != "L"]
                steps += 1
        step_list.append(steps)
    print(*numpy.lcm.reduce(step_list))


if __name__ == "__main__":
    print(analyse_file("input.txt"))
