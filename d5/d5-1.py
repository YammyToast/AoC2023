def analyse_file(__filename: str):
    groups = []
    seeds = []
    with open(__filename) as f:
        seeds = f.readline().strip("\n").split(" ")[1:]
        for line in f:
            if line == "\n":
                groups.append([])
                # Skip Line in File.
                f.readline()
            else:
                # Range Lower, Range Upper, Change
                values = line.strip("\n").split(" ")
                groups[-1].append(
                    [
                        int(values[1]),
                        int(values[1]) + int(values[2]),
                        int(values[0]) - int(values[1]),
                    ]
                )
    results = []
    for seed in seeds:
        running = int(seed)
        for group in groups:
            for filter in group:
                if running >= filter[0] and running <= filter[1]:
                    running = running + filter[2]
                    break
        results.append(running)
    print(min(results))


if __name__ == "__main__":
    print(analyse_file("input.txt"))
