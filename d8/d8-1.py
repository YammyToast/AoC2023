import re


def analyse_file(__filename: str):
    with open(__filename) as f:
        lines = f.readlines()
    instructions = list(lines[0].strip("\n"))
    raw_destinations = [c.strip("\n").split(" = ") for c in lines[2:]]
    destinations = {}
    for dest in raw_destinations:
        destinations[dest[0]] = tuple(re.sub("[() ]", "", dest[1]).split(","))
    loc = "AAA"
    steps = 0
    while loc != "ZZZ":
        for instruction in instructions:
            if loc == "ZZZ":
                break
            loc = destinations[loc][instruction != "L"]
            steps += 1

    print(loc, steps)


if __name__ == "__main__":
    print(analyse_file("input.txt"))
