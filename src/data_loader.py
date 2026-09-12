import os
import pandas as pd
import numpy as np

def load_area_data (file_path):

    # Loads and cleans the Area-wise (Rural vs Urban) Unemployment dataset.

    if not os.path.exists (file_path):
        raise FileNotFoundError (f"File not found at: {file_path} !!")

    df = pd.read_csv (file_path)
    df.dropna (how = "all",inplace = True)
    df.columns = df.columns.str.strip ()

    rename_mapping = {
        "Region": "State",
        "Date": "Date",
        "Frequency": "Frequency",
        "Estimated Unemployment Rate (%)": "Unemployment_Rate",
        "Estimated Employed": "Employed",
        "Estimated Labour Participation Rate (%)": "Labour_Participation_Rate",
        "Area": "Area",
    }
    df.rename (columns = rename_mapping,inplace = True)
    df ["Date"] = pd.to_datetime(df["Date"],dayfirst = True,errors = "coerce")
    df.dropna (subset = ["Unemployment_Rate"],inplace = True)

    df ["Year"] = df ["Date"].dt.year
    df ["Month_Name"] = df ["Date"].dt.month_name ()
    df ["Month_Num"] = df ["Date"].dt.month
    df ["Is_Lockdown"] = df ["Date"].between ("2020-03-24","2020-06-30")

    return df

def load_geo_data (file_path):

    # Loads and cleans the Regional & Geographic Unemployment dataset.

    if not os.path.exists (file_path):
        raise FileNotFoundError (f"File not found at: {file_path} !!")

    df = pd.read_csv (file_path)
    df.columns = df.columns.str.strip ()

    # NOTE: In Kaggle dataset, 'longitude' holds Latitude (~15-33) and 'latitude' holds Longitude (~71-92)

    rename_mapping = {
        "Region": "State",
        "Date": "Date",
        "Frequency": "Frequency",
        "Estimated Unemployment Rate (%)": "Unemployment_Rate",
        "Estimated Employed": "Employed",
        "Estimated Labour Participation Rate (%)": "Labour_Participation_Rate",
        "Region.1": "Zone",
        "longitude": "Latitude",   # Corrected mapping
        "latitude": "Longitude",   # Corrected mapping
    }
    df.rename (columns = rename_mapping,inplace = True)
    df ["Date"] = pd.to_datetime (df ["Date"],dayfirst = True,errors = "coerce")
    df.dropna (subset = ["Unemployment_Rate"],inplace = True)

    df ["Year"] = df ["Date"].dt.year
    df ["Month_Name"] = df ["Date"].dt.month_name ()
    df ["Month_Num"] = df ["Date"].dt.month
    df ["Is_Lockdown"] = df ["Date"].between ("2020-03-24","2020-06-30")

    return df

if __name__ == "__main__":
    area_path = os.path.join ("data","Unemployment in India.csv")
    geo_path = os.path.join ("data","Unemployment_Rate_upto_11_2020.csv")
    df_area = load_area_data (area_path)
    df_geo = load_geo_data (geo_path)
    print ("Coordinates properly mapped. Ready !!")