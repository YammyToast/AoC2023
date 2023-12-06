import copy

# From: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/


def chunk_seeds(l):
    for i in range(0, len(l), 2):
        yield [int(l[i]), int(l[i]) + int(l[i + 1])]


def analyse_file(__filename: str):
    groups = []
    seed_groups = []
    with open(__filename) as f:
        seeds = f.readline().strip("\n").split(" ")[1:]
        seed_groups = list(chunk_seeds(seeds))
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

    for seed_range in seed_groups:
        running = []
        next = [seed_range]
        for group in groups:
            running = copy.deepcopy(next)
            next = []
            for seed in running:
                for filter in group:
                    out_range = range(
                        max(filter[0], seed[0]), min(filter[1], seed[-1]) + 1
                    )
                    if len(out_range) > 0:
                        next.append(
                            [
                                int(out_range[0]) + int(filter[2]),
                                int(out_range[-1]) + int(filter[2]),
                            ]
                        )
        results.extend(running)
    print(sorted(results, key=lambda x: x[0]))
    # for group in groups:
    #     running = next
    #     next = []
    #     for filter in group:
    #         out_range = range(max(filter[0], running[0]), min(filter[-1], running[-1])+1)
    #         if len(out_range) > 0:
    #             running.append(out_range)


if __name__ == "__main__":
    print(analyse_file("input.txt"))
