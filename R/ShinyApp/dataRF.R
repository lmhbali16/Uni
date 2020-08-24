library(GEOquery)
library(R.utils)
library(reshape2)
library(ggplot2)
library(limma)
library(dplyr)
library(shiny)
library(shinythemes)


kidney_data = read.csv("GSE120396_expression_matrix.csv")
rownames(kidney_data) <- kidney_data[,1]
kidney_data = kidney_data[,2:length(kidney_data)]


clinical_outcome <-getGEO("GSE120396")
clinical_outcome<- clinical_outcome$GSE120396_series_matrix.txt.gz

rejection_status  <- clinical_outcome$characteristics_ch1.1
rejection_status <- unlist(lapply( strsplit(as.character(rejection_status), ": " ) , `[[` , 2)  )