import re

def collect_numbers(__text: str):
    first = None
    last = None
    chars = [*__text]
    for char in chars:
        if char.isdigit():
            if first == None:
                first = char
            last = char
    return str(first) + str(last)


def analyse_file(__filename: str):
    with open(__filename) as f:
        lines = f.readlines()
    sum = 0
    for line in lines:
        sum += int(collect_numbers(line))
    return sum

if __name__ == '__main__':
    print(analyse_file('input.txt'))