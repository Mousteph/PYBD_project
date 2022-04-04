import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helpers.utils import load_weather_data, load_calls_correlation_data, remove_outliers

import numpy as np

calls = load_calls_correlation_data()
weather = load_weather_data()


def display_correlation_plot(freq="W", start=None, end=None):
    calls_date = calls.loc[start:end]
    weather_data = weather.loc[start:end]

    nb_calls = calls_date.resample(freq).size()
    avg = weather_data.tavg.resample(freq).mean()

    nb_calls = remove_outliers(nb_calls)
    avg = remove_outliers(avg)

    corr = np.corrcoef(nb_calls, avg)[0][1]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=nb_calls.index, y=nb_calls, name="Appels"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=nb_calls.index, y=avg, name="Temperature"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=f"Corrélation entre le nombre d'appels et la temperature moyenne {round(corr * 100, 2)}%"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Nombre d'appels", secondary_y=False)
    fig.update_yaxes(title_text="Temperature moyenne", secondary_y=True)

    return fig
