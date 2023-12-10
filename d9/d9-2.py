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
        for i in enumerate(stages[::-1]):
            next = int(i[1][0]) - next
        sum += next
    print(sum)


if __name__ == "__main__":
    print(analyse_file("input.txt"))
