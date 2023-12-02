import re

pseudo_map = {
    "one": "o1ne",
    "two": "t2wo",
    "three": "t3hree",
    "four": "f4our",
    "five": "f5ive",
    "six": "s6ix",
    "seven": "s7even",
    "eight": "e8ight",
    "nine": "n9ine"
}

def add_pseudo_digits(__text: str):
    text = __text
    for m in pseudo_map.items():
        text = re.sub(m[0], m[1], text)
    return text

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


def read_file(__filename: str):
    with open(__filename) as f:
        lines = f.readlines()
    sum = 0
    for line in lines:
        modified = add_pseudo_digits(line)
        sum += int(collect_numbers(modified))
    return sum

if __name__ == '__main__':
    print(read_file('input.txt'))