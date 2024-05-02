## It takes as input a bray-courtis matrix bewteen metagenome samples
## uses MirKAT library from Wilson et al., (2020). MiRKAT: kernel machine regression-based global association tests for the microbiome. Bioinformatics, 37(11), 1595–1597. https://doi.org/10.1093/bioinformatics/btaa951
## Executable from Rstudio given absolute path to files
library(MiRKAT)
bray_curtis <- read.delim("c:/Users/cesar/OneDrive/Escritorio/UNAM/Proyecto/Archivos_finales/2024-2/MiRKAT/Bray_courtis_Species.txt", sep="\t")
print(bray_curtis)
# Assuming all columns except the first are numeric data
bray_curtis_matrix <- as.matrix(bray_curtis[, -1])
if(any(!is.finite(bray_curtis_matrix))) {
  warning("The matrix contains non-finite values (NA, NaN, or Inf).")
}
# Generate the kernel matrix
rownames(kernel_matrix) <- sample_names
colnames(kernel_matrix) <- sample_names
# Generate the kernel matrix
kernel_matrix <- D2K(bray_curtis_matrix)
print(kernel_matrix)
# Example: Saving kernel_matrix as a tsv file with row and column names
write.table(kernel_matrix, "c:/Users/cesar/OneDrive/Escritorio/UNAM/Proyecto/Archivos_finales/2024-2/MiRKAT/kernel_matrix3.tsv", row.names = TRUE, sep="\t")

##########################################################################






