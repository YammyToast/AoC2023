import re


def range_overlap(__range1, __range2):
    return len(set(__range1).intersection(__range2)) != 0


def collect_numbers(__line1, __line2, __line3):
    return (
        list(re.finditer(r"[0-9]+", __line1))
        + list(re.finditer(r"[0-9]+", __line2))
        + list(re.finditer(r"[0-9]+", __line3))
    )


def analyse_file(__filename: str):
    lines = []
    with open(__filename) as f:
        for line in f:
            lines.append(line.rstrip(r"\n"))

    it = 1
    sum = 0

    while it < (len(lines) - 1):
        symbols = re.finditer(r"""[-!$%^&*()_+|~=`{}\[\]:";'<>?,\/\@\#]""", lines[it])

        numbers = [
            (range(x.span()[0], x.span()[1]), x.group(0))
            for x in collect_numbers(lines[it - 1], lines[it], lines[it + 1])
        ]

        for char in symbols:
            index_range = range(char.span()[0] - 1, char.span()[1] + 1)
            for number in numbers:
                sum += range_overlap(number[0], index_range) * int(number[1])
        it += 1
    return sum


if __name__ == "__main__":
    print(analyse_file("input.txt"))
    print("DAYTHREE!")
