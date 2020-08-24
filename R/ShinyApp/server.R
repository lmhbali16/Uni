library(GEOquery)
library(R.utils)
library(reshape2)
library(ggplot2)
library(limma)
library(dplyr)
library(tidyverse)
library(shiny)
library(psych)







server <- function(input, output){
  
  output$pca <- renderPlot({pca()})
  output$summary <- renderTable(psych::describe(t(getdata())))
  output$data <- DT::renderDataTable({getdata()})
  output$label <- renderText({getlabel()})
  
  result1 <- c()
  result2 <- c()
  
  boxplotResult <- eventReactive(input$action, {
    withProgress(message = "Wait",min = 0,max = 100,{
    result1 <- experiment(input$cv1,input$tree1,input$var1,input$rep1)
    result2 <- experiment(input$cv2,input$tree2,input$var2,input$rep2)
    par(mfrow=c(1,2))
    boxplot(result1, main = "Performance of Model", xlab="Random Forest 1",ylab="Accuracy",col="green")
    boxplot(result2, main = "Performance of Model", xlab="Random Forest 2",ylab="Accuracy",col="blue")})
  })
  
  output$boxplot <- renderPlot({boxplotResult()})
  
  
  
}