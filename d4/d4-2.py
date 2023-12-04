import re


def count_line_matches(__winning_numbers, __card_numbers):
    # print(__winning_numbers, " | ",  __card_numbers)
    # winning_numbers = __winning_numbers.split(" ")
    winning_numbers = set(re.split("\s+", __winning_numbers))
    card_numbers = set(re.split("\s+", __card_numbers))
    shared = list(card_numbers.intersection(winning_numbers))
    return 2 ** (len(shared) - 1) if len(shared) > 0 else 0
    # return 2**(len(shared)-1)


def analyse_file(__filename: str):
    lines = []
    with open(__filename) as f:
        for line in f:
            split = re.split("[|:]", line.strip("\n"))
            winning_numbers = set(re.split("\s+", split[1].strip()))
            card_numbers = set(re.split("\s+", split[2].strip()))
            shared = list(card_numbers.intersection(winning_numbers))
            lines.append([len(shared), 1])

    sum = 0
    for i, line in enumerate(lines):
        print("Current:", i,  " | Next: ", range(i+1, line[1]))
        for it in range(i+1, i+1+line[0]):
            lines[it][1] += line[1] 
        sum += line[1]
    return sum


if __name__ == "__main__":
    print(analyse_file("input.txt"))
