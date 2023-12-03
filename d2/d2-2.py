import re

config = {"red": 12, "green": 13, "blue": 14}


def find_product(__text: str):
    text = re.split(r"[^\w]+", __text)
    counter = {"red": 0, "green": 0, "blue": 0}
    it = 3
    while it < len(text):
        if counter[text[it]] < int(text[it-1]):
            counter[text[it]] = int(text[it-1])
        it += 2
    return (counter["red"] * counter["green"] * counter["blue"])


def analyse_file(__filename: str):
    with open(__filename) as f:
        lines = f.readlines()
    sum = 0
    for line in lines:
        sum += find_product(line)

    return sum


if __name__ == '__main__':
    print(analyse_file('input.txt'))
