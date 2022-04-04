import numpy as np
import pandas as pd


def remove_outliers(x, standardize=False):
    data = x.fillna(method='ffill').fillna(method='backfill')
    data = data.where(np.abs((data - data.mean()) / data.std()) <= 2, np.nan)
    data = data.fillna(method='ffill').fillna(method='backfill')

    if standardize:
        return (data - data.min()) / (data.min() - data.max())

    return data


def load_calls_correlation_data():
    return pd.read_csv("NYPD_Calls_data.csv", index_col="INCIDENT_DATE", parse_dates=True)


def load_weather_data():
    return pd.read_csv("meteoNY.csv", index_col="date", parse_dates=True)
