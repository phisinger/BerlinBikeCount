import pandas as pd

data_location = pd.read_excel(
    "../data/radzaehlung_berlin.xlsx", sheet_name="Standortdaten", engine="openpyxl")
data_2012 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2012", engine="openpyxl")
data_2013 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2013", engine="openpyxl")
data_2014 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2014", engine="openpyxl")
data_2015 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2015", engine="openpyxl")
data_2016 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2016", engine="openpyxl")
data_2017 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2017", engine="openpyxl")
data_2018 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2018", engine="openpyxl")
data_2019 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2019", engine="openpyxl")
data_2020 = pd.read_excel("../data/radzaehlung_berlin.xlsx",
                          sheet_name="Jahresdatei 2020", engine="openpyxl")

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
                "17-SZ-BRE-O": "breo",
                "17-SZ-BRE-W": "brew",
                "20-TS-MAR-N ": "marn",
                "20-TS-MAR-S": "mars",
                "21-NK-MAY": "mayb",
                "23-TK-KAI": "kais",
                "06-FK-FRA-O": "frao",
                "06-FK-FRA-W": "fraw"}

# %% [markdown]
# We change columns and rows: After the transformation, we have a column with station names, and a column with corresponding number of cyclists at this point in time (DateTime column). This tranformation is made by the `table.melt` command.
# Moreover we change station abbrevations according to the dectionairy defined in previous cell.

# %%
output_tables = []
for table in counting_tables:
    table.rename(columns=columns_dict, inplace=True)
    temp_table = table.melt(
        id_vars='DateTime', value_name="cyclists", var_name="station")
    # print(temp_table)
    output_tables.append(temp_table.dropna(subset=['DateTime']))


data_location.replace({"Zaehlstelle": columns_dict}, inplace=True)

# combine all output_tables with a union to one big data set
data = pd.concat(output_tables, ignore_index=True)

# drop duplicate rows
data = data.drop_duplicates(
    subset=["DateTime", "station"], keep='last', ignore_index=True)

# drop all rows with error or null values
data_clean = data
data_clean.loc[data.cyclists == -1, 'cyclists'] = np.nan
data_clean.dropna(inplace=True)

# calculate sum of cyclists per day
# split in day, month, year, station
# then recompile everything back

# split dataset by station name

# save data with pickle or csv
