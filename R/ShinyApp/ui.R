library(shiny)
library(shinythemes)
library(tidyverse)
source("Tab.R", local = TRUE)
source("server.R", local = TRUE)
#source("dataRF.R", local = TRUE)




ui <- fluidPage(
  responsive =TRUE,
  theme = shinytheme("cerulean"),
  navbarPage(
    "Random Forest Report 2",
    tab1,
    tab2
  )
)



shinyApp(ui = ui, server = server)