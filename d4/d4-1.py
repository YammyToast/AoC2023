import re

def count_line_matches(__winning_numbers, __card_numbers):
    # print(__winning_numbers, " | ",  __card_numbers)
    # winning_numbers = __winning_numbers.split(" ")
    winning_numbers = set(re.split("\s+", __winning_numbers))
    card_numbers = set(re.split("\s+", __card_numbers))
    shared = list(card_numbers.intersection(winning_numbers))
    return 2**(len(shared)-1) if len(shared) > 0 else 0
    # return 2**(len(shared)-1)


def analyse_file(__filename: str):
    lines = []
    with open(__filename) as f:
        lines = f.readlines()
    sum = 0
    for line in lines:
        split = re.split("[|:]", line.strip("\n"))
        sum += count_line_matches(split[1].strip(), split[2].strip())
    return sum

if __name__ == "__main__":
    print(analyse_file("input.txt"))
