### Code use to create scatter plot from aldex2 differential abundance
### results obtain with the pipeline created by Siranosian, B., & Moss, E. (2023). 
### Kraken2 Classification. Zendo. https://zenodo.org/records/8015292
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# It takes as input the original table. It works with any taxonomical order
# results
data=pd.read_table('aldex_result_genus.tsv', sep="\t")
df=data
def plot_association_graph(df):
    #df['effect'] = pd.to_numeric(df['effect'], errors='coerce')
    #df = df.dropna(subset=['effect'])
    
    fdr_threshold = -np.log10(1E-03) # Obtional as desiered
    
    fig, ax = plt.subplots()
                                                # Changing this number will select the number of taxa names to display
    top_positive = df[df['effect'] > 0].nlargest(8, 'effect')['taxa'].values
    top_negative = df[df['effect'] < 0].nsmallest(8, 'effect')['taxa'].values

    for _, row in df.iterrows():
        #x_val = -np.log10(row['wi.eBH']) # this four lines change the axis-order
        #y_val = -np.log10(row['we.eBH'])
        x_val = -np.log10(row['we.eBH'])
        y_val = -np.log10(row['wi.eBH'])
        if row['effect'] > 0 and x_val >= fdr_threshold and y_val >= fdr_threshold:
            color = 'blue'
        elif row['effect'] < 0 and x_val >= fdr_threshold and y_val >= fdr_threshold:
            color = 'red'
        else:
            color = 'gray'
        ax.scatter(x_val, y_val, color=color)
        if row['taxa'] in top_positive or row['taxa'] in top_negative:
            ax.annotate(row['taxa'], (x_val, y_val))

    ax.axhline(y=fdr_threshold, color='gray', linestyle='--')
    ax.axvline(x=fdr_threshold, color='gray', linestyle='--')

    ax.set_xlabel('-log10(Welch FDR)')
    ax.set_ylabel('-log10(Wilcoxon FDR)')

    plt.show()

if __name__ == "__main__":
    plot_association_graph(df)

#    ax.set_xlabel('-log10(Wilcoxon FDR)')
#    ax.set_ylabel('-log10(Welch FDR)')
#    
