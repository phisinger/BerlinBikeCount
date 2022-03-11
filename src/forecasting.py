# import packages
from prophet import Prophet
import pandas as pd
import os

pd.DataFrame()

# import data
data_dict = {}
station_list = [station.split("_")[0]
                for station in os.listdir("data/prepared-data") if station != "location_data.csv"]
for station_name in station_list:
    read_data = pd.read_csv(
        filepath_or_buffer="data/prepared-data/" + station_name + "_data.csv")
    data_dict.update({station_name: read_data})
print("read in data done")

# In the following for loop, the following 3 steps are made for every station:
# 1. train model
# 2. predict next 5 years
# 3. save the predicted values

predicted_data_dict = {}
for station_name in station_list:
    # initialize and train data
    model_prophet = Prophet()
    model_prophet.fit(data_dict[station_name])

    # building array for prediction
    future_dates = pd.date_range(
        '2021-01-01', periods=(265*5), freq='D').to_frame(name="ds")
    print(future_dates.head())

    # predict the cyclists for the next years and collect all forecasts in this dict for further processing
    forecast = model_prophet.predict(future_dates)
    predicted_data_dict.update({station_name: forecast})

    # save predicted data
    forecast.to_csv(
        path_or_buf="data/predicted-data/" + station_name + "_predicted_data.csv")

    print(station_name + " done")
