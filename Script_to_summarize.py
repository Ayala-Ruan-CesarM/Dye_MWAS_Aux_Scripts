import argparse
import csv
import os
from collections import defaultdict

def main():
    """
    Sumarize pyseer gene hits if data is equal bewteen hits
    e.g Two hits "rpoD" with same statistical values will be merge and adding
    as hits.

    Args: input data: Gene_Hits.txt

    Return : None
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input file name")
    args = parser.parse_args()

    # Read in the file
    data = []
    with open(args.filename) as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            data.append(row)

    # Sort the data by the first column
    data.sort(key=lambda x: x[0])

    # Summarize the data
    summarized_data = defaultdict(list)
    for row in data:
        gene_id = row[0]
        if gene_id.isupper():
            key = gene_id
        else:
            key = gene_id.split("_")[0]
        if len(row) != 6:
            summarized_data[key].append(row)
        else:
            values = tuple(row[2:])
            for i, (k, v) in enumerate(summarized_data.items()):
                if k == key:
                    for j, row2 in enumerate(v):
                        if tuple(row2[2:]) == values:
                            v[j][1] = int(v[j][1]) + int(row[1])
                            break
                    else:
                        summarized_data[key].append(row)
                    break
            else:
                summarized_data[key].append(row)

    # Write out the summarized data
    with open("Sum" + args.filename , "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        for k, v in summarized_data.items():
            for row in v:
                writer.writerow(row)

if __name__ == "__main__":
    main()
