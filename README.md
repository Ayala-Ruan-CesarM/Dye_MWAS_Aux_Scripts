# Dye_MWAS_Aux_Scripts
This repository contains all auxiliary scripts used to analyze enviromental metagenomes positive for the textil dye degradation phenotype in a Microbiome wide association study conducted as part of my Master Degree at the National Autonomus University of Mexico at the Lab 14 under Sánchez-Reyes tutorship.

## How to use Remove_HiC.sh
```
Bash Remove_HiC.sh -i Original_HiC_Sequences.fasta -o Output_HiC_Sequences.fasta

# Currently it removes the chimeric sites GATCGATC AATTAATT GATCAATT
# But those can be change in the script to accomodate needs
```
## How to use Gene_Hits_Annotation_Args.py
```
python Gene_Hits_Annotation_Args.py -i Gene_Hits.txt -b annotation_output.txt -o file_name.txt -k KOs.kegg

# Gene_Hits.txt --> Is a tab file result from annotate_hits.py
# annotation_output.txt --> The annotation output of the hypothetical proteins with diamond/blastp
# KOs.kegg --> KOs IDs and it's annotation
```
## How to use VolcanoPlot.py
```
python VolcanoPlot.py -i associated_kmers.txt -o filename -t 1E-08

# associated_kmers.txt --> Is a tab file result of the association model
# "-o" does not require extension as the jpg is added automatically 
# "-t" or threshold is used to draw the significance line
```
## How to use QQplot.py
```
python QQplot.py -i associated_kmers.txt -o filename
# associated_kmers.txt --> Is a tab file result of the association model
# "-o" does not require extension as the jpg is added automatically 
```
## How to use Script_to_summarize.py
```
python Script_to_summarize.py Gene_Hits.txt
# Gene_Hits.txt --> Is a tab file result from annotate_hits.py
```
## How to use Taxonomic_Scatter_ploy.py
```
python Taxonomic_Scatter_ploy.py -i aldex_result_genus.tsv
# aldex_result_genus.tsv is the output from AlDEX2
```
## How to use VeenDiagram.R
```
# It is design to be used with Rstudio on Windows or similar.
# As input requires a tab separeted file with headers according to the condition
# It was desing to analyze the Gene_hits.txt annotation IDs in each condition not the sequence
# The library(VennDiagram) only can draw up to 5 conditions
# Load the data to the "data" dataframe
# data <- read.table("C:/PATH_To_File.tsv", sep="\t", header=TRUE)
# Create a list with each conditon
# gene_set1 <- na.omit(data$THE_NAME_OF_YOUR_CONDITION)
```
## How to use Generar_KernelMatrix_fromBray.R
```
# It is design to be used with Rstudio on Windows or similar.
# As input requires the a distance metric e.g. Bray-Courtis output of ALDEX2
# Only need to modify the PATH to the input and output variables
# input:
# bray_curtis <- read.delim("c:/PATH_TO_/Bray_courtis_table.txt", sep="\t")
# output:
# write.table(kernel_matrix, "c:/PATH_TO_/kernel_matrix.tsv", row.names = TRUE, sep="\t")
```
