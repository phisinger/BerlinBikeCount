import streamlit as st
import os
import pandas as pd
from datetime import datetime

st.title("Cyclists forecast Berlin")
st.write("...Description...")

# Read in locations
location_data = pd.read_csv("data/prepared-data/location_data.csv")
location_dict = location_data.loc[:, ].to_dict('list')
station_dict = {}
for i in range(len(location_dict['Zaehlstelle'])):
    station_dict.update(
        {location_dict["Beschreibung - Fahrtrichtung"][i]: location_dict['Zaehlstelle'][i]})

# selecting station and prediction date
selected_station = st.selectbox(
    "Select your counting station", station_dict.keys())

min_date = datetime.strptime("2021-01-01", '%Y-%m-%d')
max_date = datetime.strptime("2024-08-17", '%Y-%m-%d')

selected_date = st.date_input(
    "Select the prediction date", min_value=min_date, max_value=max_date)

st.write(station_dict[selected_station])
st.write(selected_date)

# Output

predicted_data = pd.read_csv(filepath_or_buffer="data/predicted-data/" +
                             station_dict[selected_station] + "_predicted_data.csv", parse_dates=["ds"])

print(predicted_data["ds"].dtypes)
print(type(selected_date))

# yhat for this day
yhat_text = "Forecasted Sum of cyclists on " + selected_date.strftime(
    "%Y-%m-%d") + ":"
st.write(yhat_text)
# st.write(str(round(predicted_data.loc[predicted_data['ds']
#          == selected_date.strftime("%Y-%m-%d"), "yhat"].item())))

st.write(str(round(predicted_data.loc[predicted_data['ds'].apply(
    lambda x: x.date()) == selected_date, "yhat"].item())))

# yhat for this week (avg)
week_dataframe = predicted_data.loc[predicted_data['ds'].apply(
    lambda x: x.isocalendar()[:2]) == selected_date.isocalendar()[:2], ["ds", "yhat"]]

week_text = "Average sum of cyclists for the week from " + week_dataframe.iloc[0]["ds"].strftime(
    "%Y-%m-%d") + " to " + week_dataframe.iloc[6]["ds"].strftime(
    "%Y-%m-%d") + ":"
st.write(week_text)
st.write(str(round(week_dataframe["yhat"].mean())))

# yhat for this month (avg)
month_dataframe = predicted_data.loc[predicted_data['ds'].apply(
    lambda x: x.timetuple()[:2]) == selected_date.timetuple()[:2], ["ds", "yhat"]]

month_text = "Average sum of cyclists for the month from " + month_dataframe.iloc[0]["ds"].strftime(
    "%Y-%m-%d") + " to " + month_dataframe.iloc[-1]["ds"].strftime(
    "%Y-%m-%d") + ":"
st.write(month_text)
st.write(str(round(month_dataframe["yhat"].mean())))

# yhat for this year (avg)
year_dataframe = predicted_data.loc[predicted_data['ds'].apply(
    lambda x: x.year) == selected_date.year, ["ds", "yhat"]]

year_text = "Average sum of cyclists for the year from " + year_dataframe.iloc[0]["ds"].strftime(
    "%Y-%m-%d") + " to " + year_dataframe.iloc[-1]["ds"].strftime(
    "%Y-%m-%d") + ":"
st.write(year_text)
st.write(str(round(year_dataframe["yhat"].mean())))

# map
print(selected_station)
map_data = (location_data.loc[location_data["Beschreibung - Fahrtrichtung"] == selected_station, [
    "Breitengrad", "Laengengrad"]]).rename(columns={"Breitengrad": "lat", "Laengengrad": "lon"})

st.map(data=map_data)

# graph of data throughout the year
st.line_chart(year_dataframe.set_index("ds").rename(
    columns={"yhat": "sum of cyclists"}).rolling(window=7, min_periods=1).mean())
