import re
import sys

# Prompt user for input
while True:
    card = input("Number: ")
    if re.match("^[0-9]+$", card) and len(card) >= 13:
        break
    # If input matches regex but length is less than 13 it is invalid
    if re.match("^[0-9]+$", card) and len(card) < 13:
        sys.exit("INVALID")

# Perform checksum on card
nums_to_multiply = 0
nums_to_add = 0

# Compute numbers to multiply (every other number)
for i in range((len(card)-2), -1, -2):
    if int(card[i]) * 2 < 10:
        nums_to_multiply += int(card[i]) * 2
    else:
        nums_to_multiply += (int(card[i]) * 2) - 9

# Compute numbers to add
for i in range(len(card)-1, -1, -2):
    nums_to_add += int(card[i])

# Make sure the check sums last number is 0
check_sum = (nums_to_add + nums_to_multiply) % 10

# If not the card is invalid
if check_sum != 0:
    sys.exit("INVALID")

# Slice first 2 digits to check what card it is
first_two = int(card[:2])

if len(card) == 15 and first_two == 34 or first_two == 37:
    sys.exit("AMEX")

mastercard = [i for i in range(51, 56)]
if len(card) == 16 and first_two in mastercard:
    sys.exit("MASTERCARD")

if len(card) == 13 or len(card) == 16 and int(card[0]) == 4:
    sys.exit("VISA")

# If none of the conditionals are met the card must be invalid
sys.exit("INVALID")