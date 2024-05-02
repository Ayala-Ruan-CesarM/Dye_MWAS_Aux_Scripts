# Proyecto entregable Python Cientifico
# Creado por Cesar Mauricio Ayala Ruan
# Estudiante segundo semestre Maestria ciencias  bioquimicas. 

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import pandas as pd
import seaborn as sns
import argparse 
import os

# 07/06/23 !!!!!! PENDIENTE
"""Implementar el script a los datos obtenidos de pyseer sin el filtrado de las secuencias
    Esto es... que las graficas se realicen con todos los datos."""


def parse_args():
        parser = argparse.ArgumentParser(description="Sumarize and create graph from pyseer output. -i option is required")
        parser.add_argument("-i", "--input_file", help = "Input file (output file from pyseer)", required=True)
        parser.add_argument("-o", "--output_file", type=str, default="Data_Filtered.txt", help = "Name of Output file to store the filtered data. Default:Data_Filtered.txt", required=None) 
        parser.add_argument("-sep", "--separator", default="\t", help="Specify the separator of the input file, Default tab")
        parser.add_argument("-q1", "--plotname", type=str, default="QQ_Plot.jpg", help="Name of the qqplot without correction, Default: QQ_Plot.jpg" )
        args = parser.parse_args()
        return args

class PyseerVisual:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = f'{output_file}.txt'

    def qq_plots(self, plotname):

        print("Drawing QQ_plot")
        # Read input file
        data = pd.read_csv(self.input_file, sep='\t', header=None, skiprows=1)
        # Selected data and apply log10 transformation
        data_selecction = np.sort(data[3].replace(0, 1e-01))
        sorted_pvalues = -np.log10(data_selecction)
        # Calculate expected p-value for a uniform distribution
        cal_expected_pvalues = pd.Series(stats.uniform.ppf(np.arange(1, len(sorted_pvalues) + 1) / len(sorted_pvalues), loc=0, scale=2))
        expected_pvalues = -np.log10(cal_expected_pvalues)
        #Create the plot (figure) with the axes
        fig, ax = plt.subplots(figsize=(9, 9))
        #Scatter plot with X (expected) and Y (observed) values, point size, color and transparency
        ax.scatter(expected_pvalues, sorted_pvalues, s=30, color="black", alpha=0.5)
        # Fit a straight line (polynomial grade 1) to the data points and plot it
        slope, intercept = np.polyfit(expected_pvalues, sorted_pvalues, 1)
        #Return evenly spaced numbers in an interval start point - end point, number of points
        x = np.linspace(expected_pvalues.min(), expected_pvalues.max(), 1000)
        y = slope * x + intercept
        ax.plot(x, y, color="red", linestyle="--", linewidth=2)
        #Set labels to the qqplot and save it
        ax.set_xlabel("Expected p-values")
        ax.set_ylabel("Observed p-values")
        ax.set_title("Quantil-Quantil plot")
        plt.savefig(f'{args.plotname}.jpg' , dpi=400)
        print("QQ plot without correction drawn")

        return None 
       
 
if __name__ == "__main__":
    args = parse_args()
    pyseer_visual = PyseerVisual(args.input_file, args.output_file)
    pyseer_visual.qq_plots(args.plotname)
