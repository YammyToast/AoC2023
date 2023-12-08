from collections import Counter
from enum import Enum
import itertools


class Cards(Enum):
    A = 13
    K = 12
    Q = 11
    T = 10
    J = 1


def analyse_file(__filename: str):
    # Match Type, Value, Text, Winning
    lines = []
    with open(__filename) as f:
        for line in f:
            text, winning = line.split()
            counter = Counter()
            digit = len(text) - 1
            value = 0
            for char in list(text):
                counter[char] += 1
                value += (15**digit) * (
                    int(char) if char not in Cards.__members__ else Cards[char].value
                )
                digit -= 1
            match_type = 1
            print("BEFORE:", counter)
            jokers = counter["J"]
            counter["J"] = 0
            counter[counter.most_common()[0][0]] += jokers
            del counter["J"]
            print("AFTER :", counter)

            match len(counter):
                case 1:
                    match_type = 7
                case 2:
                    match_type = 6 if counter.most_common(1)[0][1] == 4 else 5
                case 3:
                    match_type = 4 if counter.most_common(1)[0][1] == 3 else 3
                case 4:
                    match_type = 2
            lines.append([str(match_type), value, text, int(winning)])
    sorted_lines = sorted(lines, key=lambda x: x[0])

    sum = 0
    it = 1
    for key, group in itertools.groupby(sorted_lines, key=lambda x: x[0]):
        sorted_in_type = sorted(list(group), key=lambda x: x[1])
        for hand in sorted_in_type:
            sum += hand[3] * it
            it += 1
    return sum


if __name__ == "__main__":
    print(analyse_file("input.txt"))
