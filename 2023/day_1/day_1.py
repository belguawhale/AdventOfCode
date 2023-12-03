import string  
# part 1
total = 0

with open("input.txt", "r") as f:
    for line in f:
        clean_line = line.strip("\n")
        just_digits = clean_line.strip(string.ascii_lowercase)
        # total += int(just_digits[0] + just_digits[-1])
        
print(total)

# part 2
import re

total = 0
digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
regex = "[0-9]|one|two|three|four|five|six|seven|eight|nine"
reversed_regex = "[0-9]|" + "one|two|three|four|five|six|seven|eight|nine"[::-1]

def extract_digit(s):
    if s in digits:
        return str(digits.index(s) + 1)
    return s

with open("input.txt", "r") as f:
    for line in f:
        clean_line = line.strip("\n")
        forward_match = re.search(regex, clean_line)
        reverse_match = re.search(reversed_regex, clean_line[::-1])
        print(forward_match, reverse_match)

        total += int(extract_digit(forward_match.group()) + extract_digit(reverse_match.group()[::-1]))
print(total)