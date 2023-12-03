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
    # Unpack string into character
    chars = [*__text]
    for char in chars:
        if char.isdigit():
            # Only ever write first once
            if first == None:
                first = char
            # Always write last as it will resolve to become the last digit
            # Write both the first and last as they may be the same index
            last = char
    # Concat numbers for sum
    return str(first) + str(last)


def analyse_file(__filename: str):
    # Open input file and read all lines into variable
    with open(__filename) as f:
        lines = f.readlines()
    sum = 0
    # Iterate over the lines in the input file
    for line in lines:
        # Use the string with pseudo digits replaced
        modified = add_pseudo_digits(line)
        # Accumulate values from the respective line
        sum += int(collect_numbers(modified))
    return sum


if __name__ == '__main__':
    print(analyse_file('input.txt'))
