#!/usr/bin/python
import sys

# Author: dank-panda
# Version: 0.1 - initial script

# Create a class so we can add some colors to the output
class colors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'


# Function to calculate the percentage and colorize the output
def calculate_percentage(value, total):
    percentage = (value * 100) / total
    if percentage >= 67:
        color = colors.green
    elif percentage <= 33:
        color = colors.red
    else:
        color = colors.yellow
    return percentage, color


# Make sure we have the right args from the command line
if len(sys.argv) < 2:
    print(colors.yellow + f"Usage: python {sys.argv[0]} <passwords_file.txt>\n" + colors.end)
    sys.exit()

passfile = sys.argv[1]

# Variables for counts
starts_upper = starts_lower = starts_number = starts_special = 0
ends_letter = ends_number = ends_special = 0
lengths = {i: 0 for i in range(5, 13)}  # Dictionary for length counts
contains_client = 0
clients = ('client', 'client1', 'client2')
num_words = 0

# Read file and process all data
with open(passfile) as file:
    lines = [line.strip() for line in file if line.strip()]  # Remove empty lines and strip whitespace

    num_words = len(lines)

    for line in lines:
        # Check starting character
        if line[0].isupper():
            starts_upper += 1
        elif line[0].islower():
            starts_lower += 1
        elif line[0].isdigit():
            starts_number += 1
        else:
            starts_special += 1

        # Check ending character
        if line[-1].isalpha():
            ends_letter += 1
        elif line[-1].isdigit():
            ends_number += 1
        else:
            ends_special += 1

        # Check word length
        length = len(line)
        if length <= 5:
            lengths[5] += 1
        elif length == 6:
            lengths[6] += 1
        elif length == 7:
            lengths[7] += 1
        elif length == 8:
            lengths[8] += 1
        elif length == 9:
            lengths[9] += 1
        elif length == 10:
            lengths[10] += 1
        elif length == 11:
            lengths[11] += 1
        else:
            lengths[12] += 1

        # Check for client names
        if any(client in line.lower() for client in clients):
            contains_client += 1

# Calculate percentages for the different categories
percent_starts_upper, colorup = calculate_percentage(starts_upper, num_words)
percent_starts_lower, colorlow = calculate_percentage(starts_lower, num_words)
percent_starts_number, colornum = calculate_percentage(starts_number, num_words)
percent_starts_special, colorspec = calculate_percentage(starts_special, num_words)

percent_ends_letter, color_ends_letter = calculate_percentage(ends_letter, num_words)
percent_ends_number, color_ends_num = calculate_percentage(ends_number, num_words)
percent_ends_special, color_ends_spec = calculate_percentage(ends_special, num_words)

# Length-based percentages
length_percentages = {length: calculate_percentage(count, num_words) for length, count in lengths.items()}
percent_client, color_client = calculate_percentage(contains_client, num_words)

# Writing the output of the calculations and colorizing
print("-" * 60)
print(" Starting Characters")
print("-" * 60)
print(f"{colorup}{starts_upper} of the {num_words} passwords start with an uppercase letter")
print(f"  [ ~ {percent_starts_upper:.2f}% ]\n{colors.end}")

print(f"{colorlow}{starts_lower} of the {num_words} passwords start with a lowercase letter")
print(f"  [ ~ {percent_starts_lower:.2f}% ]\n{colors.end}")

print(f"{colornum}{starts_number} of the {num_words} passwords start with a number")
print(f"  [ ~ {percent_starts_number:.2f}% ]\n{colors.end}")

print(f"{colorspec}{starts_special} of the {num_words} passwords start with a special character")
print(f"  [ ~ {percent_starts_special:.2f}% ]\n{colors.end}")

print("-" * 60)
print(" Ending Characters")
print("-" * 60)

print(f"{color_ends_letter}{ends_letter} of the {num_words} passwords end with a letter")
print(f"  [ ~ {percent_ends_letter:.2f}% ]\n{colors.end}")

print(f"{color_ends_num}{ends_number} of the {num_words} passwords end with a number")
print(f"  [ ~ {percent_ends_number:.2f}% ]\n{colors.end}")

print(f"{color_ends_spec}{ends_special} of the {num_words} passwords end with a special character")
print(f"  [ ~ {percent_ends_special:.2f}% ]\n{colors.end}")

print("-" * 60)
print(" Word Length")
print("-" * 60)

for length in range(5, 13):
    color = locals().get(f"color_length{length}", colors.end)
    print(f"{color}{lengths[length]} of the {num_words} passwords have {length} letters")
    print(f"  [ ~ {length_percentages[length][0]:.2f}% ]\n{colors.end}")

print("-" * 60)
print(" Client Name")
print("-" * 60)

print(f"{color_client}{contains_client} of the {num_words} passwords have the client's name")
print(f"  [ ~ {percent_client:.2f}% ]\n{colors.end}")
