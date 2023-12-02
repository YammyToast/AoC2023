import re

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
        # Accumulate values from the respective line
        sum += int(collect_numbers(line))
    return sum


if __name__ == '__main__':
    print(analyse_file('input.txt'))
