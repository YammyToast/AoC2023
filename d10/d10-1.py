import numpy

# N E S W
dir_map = {
    "|": (1, 0, 1, 0),
    "-": (0, 1, 0, 1),
    "L": (1, 1, 0, 0),
    "J": (1, 0, 0, 1),
    "7": (0, 0, 1, 1),
    "F": (0, 1, 1, 0),
}


def analyse_file(__filename: str):
    lines = []
    it = 0
    start_loc = 0
    with open(__filename) as f:
        for line in f:
            lines.append(x := list(line.strip("\n")))
            if "S" in x:
                start_loc = (it, x.index("S"))
            it += 1
    flow = numpy.zeros(shape=(len(lines), len(lines[0])))
    # print(lines[0],"\n",flow[0])
    print(lines[start_loc[0]][start_loc[1]])


if __name__ == "__main__":
    print(analyse_file("input.txt"))
