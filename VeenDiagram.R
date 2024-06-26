## Script to analize annotation results (gene IDs as text e.g. UNIREF90_UPI100089X) bewteen conditions
## Created to be executable from RStudio
library(VennDiagram)
# Load your data
# Read the tab-separated file
data <- read.table("C:/Users/cesar/OneDrive/Escritorio/UNAM/Proyecto/Archivos_finales/2024-2/MetaTranscriptoma/Results_Annotados_WTrans.tsv", sep="\t", header=TRUE)

# Ensure all gene IDs are converted to lowercase for case-insensitive comparison
data <- lapply(data, tolower)
data <- lapply(data, tolower)

# Create a list of gene sets
gene_set1 <- na.omit(data$Microbioma_Filogenetic)
gene_set2 <- na.omit(data$Microbioma_Genetic)
gene_set3 <- na.omit(data$Microbioma_Dissimilarity)
gene_set4 <- na.omit(data$Meta_Transcriptome)
gene_set5 <- na.omit(data$MetaCore_Filogenetic)
gene_set6 <- na.omit(data$MetaCore_Genetic)
gene_set7 <- na.omit(data$MetaCore_Dissimilarity)

# Filter out empty or double-quote entries from each gene set
gene_set1 <- gene_set1[gene_set1 != ""]
gene_set2 <- gene_set2[gene_set2 != ""]
gene_set3 <- gene_set3[gene_set3 != ""]
gene_set4 <- gene_set4[gene_set4 != ""]
gene_set5 <- gene_set5[gene_set5 != ""]
gene_set6 <- gene_set6[gene_set6 != ""]
gene_set7 <- gene_set7[gene_set7 != ""]



# Specify custom colors for each group
group_colors <- c("red", "green", "blue")  # You can change these colors as needed

# Create a Venn diagram with custom colors
# Here It can be possible to compare up to 5 conditions only
venn_result <- venn.diagram(
  x = list(
    "MWAS Filogenético" = gene_set1,
    "MWAS Genético" = gene_set2,
    "MWAS Desemejanza" = gene_set3
  ),
  category.names = c("Filogenético", "Genético", "Desemejanza"),
  filename = "C:/Users/cesar/OneDrive/Escritorio/UNAM/Proyecto/Archivos_finales/2024-2/MetaTranscriptoma/venn_diagramtest.png",
  output = TRUE,
  #category.col = group_colors  # Assign custom colors to each group
  col = "black",  # Color of circle edges
  fill = group_colors,  # Fill colors inside the circles
)
## obtaion the shared gene IDs bewteen sets, totally customizable
shared_1_2 <- intersect(gene_set5, gene_set7)
print(shared_1_2)
shared_1_3 <- intersect(gene_set5, gene_set6)
print(shared_1_3)
shared_2_3 <- intersect(gene_set6, gene_set7)
print(shared_2_3)
shared_1_2_3 <- Reduce(intersect, list(gene_set5, gene_set6, gene_set7))
print(shared_1_2_3)
