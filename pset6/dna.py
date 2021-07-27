from csv import reader, DictReader
from sys import argv, exit


def main():

    # check for proper usage
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # open files
    with open(f'{argv[1]}', 'r') as csvfile:
        reader = DictReader(csvfile)
        dict_list = list(reader)

    with open(f'{argv[2]}', 'r') as file:
        sequence = file.read()

    # find longest run of repeats for each STR
    max_counts = []
    for i in range(1, len(reader.fieldnames)):
        STR = reader.fieldnames[i]
        max_counts.append(0)

        # loop through sequence
        for j in range(len(sequence)):
            STR_count = 0

            # if match, start counting
            if sequence[j: (j + len(STR))] == STR:
                k = 0
                while sequence[(j + k): (j + k + len(STR))] == STR:
                    STR_count += 1
                    k += len(STR)

                # if new max, update
                if STR_count > max_counts[i - 1]:
                    max_counts[i - 1] = STR_count

    # compare against data
    for i in range(len(dict_list)):
        matches = 0
        for j in range(1, len(reader.fieldnames)):
            if int(max_counts[j - 1]) == int(dict_list[i][reader.fieldnames[j]]):
                matches += 1
            if matches == (len(reader.fieldnames) - 1):
                print(dict_list[i]['name'])
                exit(0)

    print('No match')


main()
