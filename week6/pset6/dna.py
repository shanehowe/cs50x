import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        # Store str's in list to pass them to function call later
        fieldnames = reader.fieldnames[1:]
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    f = open(sys.argv[2])
    sequence = f.read()

    # TODO: Find longest match of each STR in DNA sequence
    longest_matches = []
    for str in fieldnames:
        longest_seq = longest_match(sequence, str)
        longest_matches.append(longest_seq)

    # Sort list to compare for equality later
    longest_matches.sort()

    # TODO: Check database for matching profiles
    for person in database:
        values = []
        for key, value in person.items():
            # Ensures name key is skipped
            if key != "name":
                values.append(int(value))
        # Sort values to compare against longest matches
        values.sort()
        # If the two lists match we have found who the DNA belongs to
        if values == longest_matches:
            print(person["name"])
            return

    # If we finish looping through database no match has been found
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()