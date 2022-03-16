# Berlin Bike Count Analysis and Forecast

![bike image by Cristiana Raluca from Pexels](./data/github_image/bike.jpg)

In this project I analyze and forecast data from the last eight years: Since 2012 sensor stations track passing cyclists at different locations. Data includes hourly measurements augmented with geographic information about the stations (coordinates and directions). You'll find the original data [here (German)](https://www.berlin.de/sen/uvk/verkehr/verkehrsplanung/radverkehr/weitere-radinfrastruktur/zaehlstellen-und-fahrradbarometer/). I uploaded the data with minimal preprocessing on [Kaggle](https://www.kaggle.com/phisinger/bike-counting-berlin).

This project contains five steps

1. Data cleaning - There are missing values and error values
2. Data exploration in SQL - Get some insights and generate interesting views
3. Data visualization with Tableau - Let's make it pretty
4. Forecasting - See into the future
5. Presenting Forecast - Ease Access with a website

## 1. Data Cleaning

As you will see, original data is published as Excel files. That's not great but acceptable. Even worse is that error values are marked by a yellow cell background. I change every colored cell to the error value '-1'. There are missing values when a station wasn't installed yet at this time. I remove these rows in SQL, see the data exploration file. Further, I transformed the data with python so it is easier to work with in SQL. For details, see [the notebook](./src/transform_excel.ipynb).

## 2. Data Exploration

In this part I explore the data arbitrarily. I try to find interesting views, especially by deriving new columns out of existing ones. You'll see that the existing columns are pretty basic: One column shows the station as a foreign key, the next one the timestamp and the third one the number of cyclists passed by in this hour. The data is grouped by years and there is one more table containing additional information about every station. Find my commented [SQL commands here](./src/SQL/DataExploration.sql)

## 3. Data Visualization

I use the generated views in Tableau to visualize interesting results. Find my interactive Tableau Dashboard [here](https://public.tableau.com/app/profile/philip.singer/viz/BerlinBikeCount/Dashboard1). Of course you think of many more charts. But these visualizations are the most important ones in my opinion.

## 4. Forecasting

First, I clean the data further in this [notebook](src/Forecasting_notebook.ipynb). My first idea was not to forecast the cyclists in a classical way but using a regression model to predict the data. Therefore I make some feature engineering. I add weekday-classification, holidays and seasons. But the performance of the gradient boosted tree was not satisfying. Because of this I tried a real forecasting model for the first time. As I had not have much experience in forecasting time series, I used Meta's prophet algorithm which has a scikit-learn-like API.  
To make the Prophet model more explainable, I calculated shapley values with the `shap` library.

## 5. Presenting Forecast

To ease the access to the forecasted data, I created a website. To operationalize the provisioning process from the excel sheet to the prediction I decided to make real python scripts next to the notebooks. See in the [src](src) folder. You'll find the web app I built with `streamlit` under this [link](https://share.streamlit.io/phisinger/berlinbikecount-website/src/streamlit_app.py). It is built completely in Python. You find the code [here](src/streamlit_app.py). I deployed it on the streamlit.io share.

---

I hope you like this project. I'm looking forward to hear your thoughts about this project. Feel free to follow and write me on [Linkedin](https://www.linkedin.com/in/philip-jonathan-singer/).
