"""Script to anotate Summarized gene hits from pyseer and anotates them
according to KOs IDs and UNIREF90 blastp anotation."""

import pandas as pd
import glob
import os
import subprocess
import re
import argparse 
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Pyseer Gene Hits to Annotations with KO and Blastp, all arguments but -u and -o are required")
    parser.add_argument("-i", "--input_file", help = "Input file (Gene_Hits file)", required=True)
    parser.add_argument("-b", "--blastp_output", help="Output file from blastp, tab separeted", required=True)
    parser.add_argument("-k", "--kegg_DB", help= "Nombre de la base de datos de KEGG",required=True )
    parser.add_argument("-u", "--uniref_DB", default= "part*.split", help="Patron comun de los archivos que contengan los identificadores de Uniref90. Default 'part*.split' ",required=None)
    parser.add_argument("-o", "--output_file", type=str, default="GeneHis_Anotated.txt", help = "Name of Output file to store the filtered data. Default:Data_Filtered.txt", required=None) 
    args = parser.parse_args()
    return args

start_time = time.time()


def getting_unirefids(input_file,blastp_output):
    print(f"Program starting with {input_file}")


    print("Getting Uniref IDs to Hypotetical proteins with blastp annotation output")    
    # Read Query file   #Query file is Genehits file after pass to KOs annotation. 
    query = pd.read_csv(input_file, sep='\t', header=None)

    # Filter rows with gene ID strings starting with "TEXDB"
    query = query[query[0].str.startswith('TEXDB')]
    #print (query[0])
    # Read Reference file
    reference_file = pd.read_csv(blastp_output, sep='\t', header=None, dtype=str)
    reference_values = reference_file.iloc[:, [0, 1]]

    annotations = []

    for index, row in query.iterrows():
        gene_id = row[0]

        annotation_row = reference_values[reference_values[0] == gene_id]

        if not annotation_row.empty:
            annotation = annotation_row.iloc[0,1]

        else:
            annotation = ''

        annotations.append(annotation)    

    query['Annotation'] = annotations

    query.to_csv("tmp1.txt", sep= '\t', header=None, index=None)
                #Aqui iba tmpout.txt
    print("UnirefIDs assigned to Hypotetical proteins")       # Hasta aqui va bien

def unirefids_annotation(uniref_DB):
    
    # Read tmpout.txt
    filetmp = pd.read_csv("tmp1.txt", sep='\t', header=None)

    # Extract column 6 as filetmp_data
    filetmp_data = filetmp.iloc[:, [6]]
    #print(filetmp_data)

    #Filtering rows with Nan values
    filetmp_data = filetmp_data.dropna(subset=[6])
    #print(filetmp_data)

    # Initialize a list to store output file names
    output_files = []
    print("UnirefIDs to gene names with Uniref90 loop")
    # Loop through each value in filetmp_data
    for value in filetmp_data[6]:
        # Create a unique output file name
        output_file = f"output_{value}.txt"
        output_files.append(output_file)
        # Call the grep command using subprocess
        #command = f"grep '{value}' UNIREF90_onlyPnames.txt > {output_file}"
        command = f"parallel -j 10 'grep -F \"{value}\" {{}} >> output_{value}.txt' ::: {uniref_DB}"    #part*.split

        subprocess.run(command, shell=True)

    # Concatenate all output files into a single file
    with open("tmp2.txt", "w") as outfile:    #This output stores the uniref annotations
        for output_file in output_files:
            with open(output_file, "r") as infile:
                outfile.write(infile.read())

    # Remove the individual output files
    for output_file in output_files:
        subprocess.run(f"rm {output_file}", shell=True)

    #Worked without this but left some residual files. Dont know why so I will remove them
    # Get a list of all files in the current directory that end with ".txt'"
    files_to_remove = glob.glob("*.txt'")

    # Loop through the list of files and remove each one
    for file in files_to_remove:
        os.remove(file)

    

def annotations_to_genefile():

    fileGHtmp = pd.read_csv("tmp1.txt", sep='\t', header=None)

    fileGHtmp_data = fileGHtmp.iloc[:, [6]] 

    fileannotated = pd.read_csv("tmp2.txt", sep='\t', header=None)
    fileannotated_data = fileannotated.iloc[:, [0]]

    # Create a new column to store the matches
    fileGHtmp[7] = ''

    for index, row in fileGHtmp_data.iterrows():
        query = row[6]
        if pd.notna(query):
            line = fileannotated_data[fileannotated_data[0].str.contains(query, regex=False)]
            if not line.empty:
                match = line.values[0][0]
                fileGHtmp.iloc[index, 7] = match

    # Save the updated filetmp to a new file
    fileGHtmp.to_csv('tmp_GHTEXDB.txt', sep='\t', header=None, index=None)
                        #Aqui este Aun es un archivo intermediario. Solo contiene los TEXDB anotados
    print("Gene names assigned to UnirefIDs")

def matchgenes_KOs(input_file,kegg_DB):
    print("Assiging KOs to genes annotated with Prokka DB")
    with open(input_file,'r') as query_file:
        query_lines = query_file.readlines()

    with open(kegg_DB, 'r') as ref_file:
        ref_lines = ref_file.readlines()

    modified_lines = []  # Initialize a list to store the modified lines

    # Loop through the query lines
    for i, query_line in enumerate(query_lines):
        # Split the line by tabs
        query_items = query_line.strip().split('\t')
        # Get the gene ID from the first column
        gene_id = query_items[0]
        # If the gene ID starts with "TEXDB", do nothing
        if gene_id.startswith("TEXDB"):
            continue
        # Otherwise, remove the "_" and the numbers from the gene ID
        else:
            gene_id = re.sub(r"_\d+", "", gene_id)
            query_items[0] = gene_id  # Update the first column with the modified gene ID

        # Loop through the reference lines to find a match for the gene ID
        for ref_line in ref_lines:
            if (gene_id + ',') in ref_line or (gene_id + ';') in ref_line:
                # If a match is found, add the reference line to the query line as the last column
                modified_line = query_line.strip() + '\t' + ref_line.strip() + '\n'
                modified_lines.append(modified_line)  # Add the modified line to the list
                break

    # Write the updated query lines that were modified to the "Output.txt" file
    with open("Output_KOS.txt", 'w') as output_file:
        output_file.writelines(modified_lines)
    print("KOs Assigned")


def merge_file(output_file):
    print(f"Writing result to: {output_file}")
    TEXDB = 'tmp_GHTEXDB.txt'
    KOS = 'Output_KOS.txt'
    command_to_merge = f"cat {TEXDB} {KOS} > {output_file}"
    subprocess.run(command_to_merge, shell=True)
    
    print("Removing temporal files")
    os.remove ("tmp1.txt")
    os.remove ("tmp2.txt")
    os.remove ("tmp_GHTEXDB.txt")
    os.remove ("Output_KOS.txt")  


    end_time = time.time()
    total_time = end_time - start_time
    print("Total time:", total_time, "seconds")
    print("Annotation complete")

if __name__ == "__main__":
    args=parse_args()
    getting_unirefids(args.input_file,args.blastp_output)
    unirefids_annotation(args.uniref_DB)
    annotations_to_genefile()
    matchgenes_KOs(args.input_file, args.kegg_DB)
    merge_file(args.output_file)