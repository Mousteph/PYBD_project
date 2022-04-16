import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helpers.utils import (
    load_weather_data,
    load_calls_correlation_data,
    remove_outliers,
)

from helpers.design import background_color, font_color, font_family, color_blue, color_green

import numpy as np

calls = load_calls_correlation_data()
weather = load_weather_data()

def display_correlation_plot(freq="M", start=None, end=None):
    nb_calls = calls.loc[start:end].resample(freq).size()
    avg = weather.loc[start:end].tavg.resample(freq).mean()

    nb_calls = remove_outliers(nb_calls)
    avg = remove_outliers(avg)
    #corr = np.corrcoef(nb_calls, avg)[0][1]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=nb_calls.index, y=nb_calls, line_color=color_blue, name="Appels"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=nb_calls.index, y=avg, line_color=color_green, name="Température"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        #title_text=f"Corrélation entre le nombre d'appels et la temperature moyenne {round(corr * 100, 2)}%",
        #title_x=0.5,
        margin=dict(l=10, r=10, b=10, t=50, pad=2),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    frequence = "mois" if freq == "M" else "semaine" if freq == "W" else "jour"

    # Set y-axes titles
    fig.update_yaxes(title_text=f"Nombre d'appels par {frequence}", secondary_y=False)
    fig.update_yaxes(title_text=f"Température moyenne par {frequence}", secondary_y=True)

    return fig
