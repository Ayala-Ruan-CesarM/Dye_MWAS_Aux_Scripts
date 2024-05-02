## Script to analyze pyseer association results in a volcano plot
## The reason to use this script is to diagnose the number of variants with negative effect size
## In principle pyseer itself removes this type of result from it but when using metagenomes
## and unitigs with --querry options from unitig-caller those type of variants remain  
## python VolcanoPlot.py --input associated_vars.txt --output figurename --threshold 1E-08 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Generate a Volcano plot from given data.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input CSV file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output figure')
parser.add_argument('-t', '--threshold', type=float, required=True, help='Pyseer Significant Threshold')
# Parse arguments
args = parser.parse_args()

# Load the data
data = pd.read_csv(args.input, sep='\t')

# Calculating -log10(pval) and storing it in a new column
data['neg_log10_pval'] = -np.log10(data['lrt-pvalue'])

# Genome-wide significance threshold
significance_threshold = -np.log10(args.threshold)

# Creating the Volcano plot
plt.figure(figsize=(10, 6))
# Using matplotlib scatter to create a mappable object
points = plt.scatter(data['beta'], data['neg_log10_pval'], c=data['beta-std-err'], cmap='viridis', edgecolor=None, alpha=0.7)

# Adding a horizontal line for the genome-wide significance threshold
plt.axhline(y=significance_threshold, color='red', linestyle='--', label=f'Significance threshold (-log10 p-value = {significance_threshold})')

# Adding vertical lines for effect size thresholds
# Can be change to any value actually
plt.axvline(x=-0.1, color='gray', linestyle='--', label='Effect size = -0.1')
plt.axvline(x=0.1, color='gray', linestyle='--', label='Effect size = 0.1')

# Enhancing the plot
#plt.title('Volcano Plot')
plt.xlabel('Effect Size')
plt.ylabel('-log10(p-value)')
plt.legend(loc='upper left')

# Creating a colorbar with the label
cbar = plt.colorbar(points, aspect=5)
cbar.set_label('Beta Standard Error')

# Save the figure
plt.savefig(f'{args.output}.jpeg', dpi=600)

print(f"Volcano plot saved to {args.output}.jpeg")
