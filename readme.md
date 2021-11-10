# Berlin Bike Count Analysis

In this project I analyze data from the last eight years: Since 2012 sensor stations track passing cyclists at different locations. Data includes hourly measurements augmented with geographic information about the stations (coordinates and directions). You'll find the data [here (german)](https://www.berlin.de/sen/uvk/verkehr/verkehrsplanung/radverkehr/weitere-radinfrastruktur/zaehlstellen-und-fahrradbarometer/).  
This project contains three steps

1. Data cleaning - There are missing values and error values
2. Data exploration in SQL - Get some insights and generate interesting views
3. Data visualization with Tableau - Let's make it pretty

## 1. Data Cleaning

As you will see, original data is published as Excel files. That's not great but acceptable. Even worse is that error values are marked by a yellow cell background. I change every colored cell to the error value '-1'. So, I can clean the data later on in SQL. Further, I transformed the data with python so it is easier to work with in SQL. For details, see [notebook](./src/transform_excel.ipynb).

## 2. Data Exploration

In this part I explore the data arbitrarily. I try to find interesting views, espacially by deriving new columns out of existing ones. You'll see that the existing columns are pretty basic: A
