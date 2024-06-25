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
```
## How to use VolcanoPlot.py
```
```
## How to use QQplot.py
```
```
## How to use Script_to_summarize.py
```
```
## How to use Taxonomic_Scatter_ploy.py
```
```
## How to use VeenDiagram.R
```
```
## How to use Generar_KernelMatrix_fromBray.R
```
```
