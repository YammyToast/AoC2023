import re

config = {"red": 12, "green": 13, "blue": 14}


def check_line(__text: str):
    text = re.split(r"[^\w]+", __text)
    it = 3
    while it < len(text):
        if config[text[it]] < int(text[it-1]):
            return 0
        it += 2
    return text[1]


def analyse_file(__filename: str):
    with open(__filename) as f:
        lines = f.readlines()
    sum = 0
    for line in lines:
        sum += int(check_line(line))
    return sum


if __name__ == '__main__':
    print(analyse_file('input.txt'))
