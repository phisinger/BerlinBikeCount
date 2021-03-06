import pandas as pd
import numpy as np
import os

# import data from excel files

data_location = pd.read_excel(
    "data/radzaehlung_berlin.xlsx", sheet_name="Standortdaten", engine="openpyxl")
data_2012 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2012", engine="openpyxl")
data_2013 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2013", engine="openpyxl")
data_2014 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2014", engine="openpyxl")
data_2015 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2015", engine="openpyxl")
data_2016 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2016", engine="openpyxl")
data_2017 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2017", engine="openpyxl")
data_2018 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2018", engine="openpyxl")
data_2019 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2019", engine="openpyxl")
data_2020 = pd.read_excel("data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2020", engine="openpyxl")
print("Reading data in done")

counting_tables = [data_2012,
                   data_2013,
                   data_2014,
                   data_2015,
                   data_2016,
                   data_2017,
                   data_2018,
                   data_2019,
                   data_2020]

# dict for replacing values of primary keys in location table
# and column names in counting tables.
# This makes the primary keys (abbrevations) more readable

columns_dict = {"12-PA-SCH": "schw",
                "02-MI-JAN-N": "jann",
                "02-MI-JAN-S": "jans",
                "13-CW-PRI": "prin",
                "18-TS-YOR-O": "yoro",
                "18-TS-YOR-W": "yorw",
                "19-TS-MON": "monu",
                "27-RE-MAR": "mark",
                "03-MI-SAN-O": "invo",
                "03-MI-SAN-W": "invw",
                "05-FK-OBB-O": "obeo",
                "05-FK-OBB-W": "obew",
                "26-LI-PUP": "paul",
                "24-MH-ALB": "albe",
                "10-PA-BER-N": "bern",
                "10-PA-BER-S": "bers",
                "15-SP-KLO-S": "klos",
                "15-SP-KLO-N": "klon",
                "17-SK-BRE-O": "breo",
                "17-SK-BRE-W": "brew",
                "20-TS-MAR-N": "marn",
                "20-TS-MAR-S": "mars",
                "21-NK-MAY": "mayb",
                "23-TK-KAI": "kais",
                "06-FK-FRA-O": "frao",
                "06-FK-FRA-W": "fraw"}

# We change columns and rows: After the transformation, we have a column with station names,
# and a column with corresponding number of cyclists at this point in time (DateTime column).
# This transformation is made by the `table.melt` command.
# Moreover we change station abbreviations according to the dictionairy defined in previous cell.


input_tables = []
for table in counting_tables:
    table.rename(columns=columns_dict, inplace=True)
    temp_table = table.melt(
        id_vars='DateTime', value_name="cyclists", var_name="station")
    # Next, we change column names. This is important, as the Prophet model only accepts column names "ds" and "y".
    temp_table.rename(
        columns={"DateTime": "ds", "cyclists": "y"}, inplace=True)
    # print(temp_table)
    input_tables.append(temp_table.dropna(subset=['ds']))


# Rename stations also in the locations table
data_location.replace({"Zaehlstelle": columns_dict}, inplace=True)

print("Transforming table done")


# combine all input_tables with a union to one big data set
data = pd.concat(input_tables, ignore_index=True)
print("Merging done")

# drop duplicate rows
data = data.drop_duplicates(
    subset=["ds", "station"], keep='last', ignore_index=True)

# drop all rows with error or null values
data_clean = data.copy()
data_clean.loc[data.y == -1, 'y'] = np.nan
data_clean.dropna(inplace=True)
print("Dropping error and nulls done")

# split dataset by station name
station_list = data_clean["station"].unique().tolist()
data_resample_dict = {}
for station_name in station_list:
    # calculate sum of cyclists per day
    data_resample = data_clean.loc[data_clean["station"] == station_name].resample(
        'D', on='ds').sum()
    data_resample_dict.update({station_name: data_resample})
print("splitting and resampling done")

# save data to csv
for station_name in station_list:
    data_resample_dict[station_name].to_csv(
        path_or_buf="data/prepared-data/" + station_name + "_data.csv")
data_location.to_csv(
    path_or_buf="data/prepared-data/location_data.csv", index=False)
print("Saving data done")
