def analyse_file(__filename: str):
    lines = []
    with open(__filename) as f:
        for line in f:
            lines.append(line.strip("\n"))
    values = []
    sum = 0
    for line in lines:
        stages = [line.split(" ")]
        while not all(v == 0 for v in stages[-1]):
            differences = []
            for i in range(0, len(stages[-1]) - 1):
                last = stages[-1]
                differences.append(int(last[i + 1]) - int(last[i]))
            stages.append(differences)
        next = 0
        for i in enumerate(stages):
            if i[0] == len(stages):
                break
            next += int(i[1][-1])
        print(next)
        for j in enumerate(stages[::-1]):
            p2nextnum = j[1][0] - p2nextnum
        sum += next
    print(sum)


if __name__ == "__main__":
    print(analyse_file("input.txt"))
