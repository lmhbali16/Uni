library(GEOquery)
library(R.utils)
library(reshape2)
library(ggplot2)
library(limma)
library(dplyr)
library(shiny)
library(tidyverse)
library(shinythemes)
library(doParallel)
library(bigstatsr)


kidney_data = read.csv("GSE120396_expression_matrix.csv")
rownames(kidney_data) <- kidney_data[,1]
kidney_data = kidney_data[,2:length(kidney_data)]



clinical_outcome <-getGEO("GSE120396")
clinical_outcome<- clinical_outcome$GSE120396_series_matrix.txt.gz

rejection_status  <- clinical_outcome$characteristics_ch1.1
rejection_status <- unlist(lapply( strsplit(as.character(rejection_status), ": " ) , `[[` , 2)  )

getlabel <- function(){
  
  
  
  yes = sum(rejection_status == "Yes")
  no = sum(rejection_status == "No")
  
  answer = paste0("yes:", yes, " no:", no, sep=" ")
  return(answer)
  
}



getdata <- function(){
  kidney_data = read.csv("GSE120396_expression_matrix.csv")
  return(kidney_data)
  
}

pca <- function(){

  
  
  gse_pca <- prcomp(t(kidney_data))
  df_toplot <- data.frame(rejection_status, 
                          pc1 = gse_pca$x[,1], pc2 = gse_pca$x[,2]  )
  
  
  g <- ggplot(df_toplot, aes(x = pc1, y = pc2, color = rejection_status)) + 
    geom_point() + labs(colour = "Label")+
    theme_minimal() +xlab("PC1")+ylab("PC2")+ggtitle("PCA of Gene Expression Data")
  return(g)
  
}



experiment <- function(cv1,tree,var,rep1){
  
  
  print(table(rejection_status))
  
  K1 = cv1
  n1 = rep1
  result1 = FBM(nrow = K1, ncol = n1)
  
  cl <- makeCluster(2)
  registerDoParallel(cl)
  X = as.matrix(t(kidney_data))
  y = rejection_status
  
  
  foreach(i= 1:n1, .packages = "tidyverse",.combine = 'c') %dopar% {
    cvSets = cvTools::cvFolds(nrow(X), K1)  # permute all the data, into 5 folds
   
    for(j in 1:K1){
      
      test_id = cvSets$subsets[cvSets$which == j]
      X_test = X[test_id, ]
      X_train = X[-test_id, ]
      y_test = y[test_id]
      y_train = y[-test_id]
      
      rf_res <- randomForest::randomForest(x = X_train, y = as.factor(y_train), mtree = tree, mtry = var)
      fit <- predict(rf_res, X_test)
      result1[j,i] = table(fit, y_test) %>% diag %>% sum %>% `/`(length(y_test))
      
    }

  }

  stopCluster(cl)
  
  result1 <- apply(result1[],2, FUN = mean)
  
  return(result1)
  
  
}