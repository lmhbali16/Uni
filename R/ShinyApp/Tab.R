library(shiny)
library(shinythemes)
library(DT)

tab1 <- tabPanel("Performance",
                 
          
                 sidebarPanel(tags$h4("RF 1"),
                              
                              sliderInput("cv1","Number of CV:",2,5,1),
                              sliderInput("tree1","Num of Tree:", 10,500,10),
                              sliderInput("var1","Num of Variables", 10,200,10),
                              sliderInput("rep1","Repitition", 5,50,5),
                              tags$h4("RF 2"),
                              sliderInput("cv2","Number of CV:",2,5,1),
                              sliderInput("tree2","Num of Tree:", 10,500,10),
                              sliderInput("var2","Num of Variables", 10,200,10),
                              sliderInput("rep2","Repitition", 5,50,5),
                              actionButton("action","Run")
                  ),
                 
                 mainPanel(h1("Boxplot of Accuracy"), verbatimTextOutput("txtout"),
                           plotOutput(outputId = "boxplot"))
        
           
)

tab2 <- tabPanel("Data Information",
                 
                 mainPanel(h1("Information About The Data"),
                           textOutput("label"),
                           tabsetPanel(
                             
                             tabPanel("PCA Plot",
                                      plotOutput("pca")),
                             tabPanel("Data Summary",
                                      tableOutput("summary")),
                             tabPanel("Raw Data",
                                      DT::dataTableOutput("data"))
                             
                             
                           ))
                 )