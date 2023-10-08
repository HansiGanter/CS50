import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py DATABASE DNASEQUENCE")

    # TODO: Read database file into a variable
    databasefile = sys.argv[1]

    database = []
    with open(databasefile) as file:
        reader = csv.DictReader(file)
        for person in reader:
            database.append(person)

    # TODO: Read DNA sequence file into a variable
    sequencefile = sys.argv[2]
    with open(sequencefile) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    longest_STRs = {}
    for STR in database[0]:
        if STR == "name":
            continue
        count = 0
        index = 0
        while sequence[index:].find(STR) != -1:
            index = index + sequence[index:].find(STR)
            sub_index = index
            sub_count = 0
            while sequence[sub_index : sub_index + len(STR)] == STR:
                sub_count = sub_count + 1
                sub_index = sub_index + len(STR)
            if sub_count > count:
                count = sub_count
            index = sub_index
        longest_STRs[STR] = count

    # TODO: Check database for matching profiles
    for person in database:
        same = True
        for item in person:
            if item == "name":
                continue
            if int(person[item]) != longest_STRs[item]:
                same = False
                break
        if same:
            print(person["name"])
            return

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
