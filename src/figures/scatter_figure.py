from helpers.utils import (
    load_calls_correlation_data,
    load_weather_data,
    remove_outliers,
)

from helpers.design import background_color, font_color, font_family, color_blue, color_green

import plotly.express as px

calls = load_calls_correlation_data()
weather = load_weather_data()


def display_correlation_scatter(freq="W", start=None, end=None):
    calls_date = calls.loc[start:end]
    weather_data = weather.loc[start:end]

    nb_calls = calls_date.resample(freq).size()
    nb_calls = remove_outliers(nb_calls)

    tavg = weather_data.tavg.resample(freq).mean()
    tavg = remove_outliers(tavg)
    wspd = weather_data.prcp.resample(freq).mean()
    wspd = remove_outliers(wspd)

    fig = px.scatter(x=tavg, y=nb_calls, trendline="ols", size=wspd,
        color_discrete_sequence=[color_blue], trendline_color_override=color_green)

    fig.update_xaxes(title_text="Temperature moyenne")
    fig.update_yaxes(title_text="Nombre d'appels")
    
    fig.update_layout(
        title_text=f"Nombre d'appels en fonction de la température moyenne",
        title_x=0.5,
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    return fig
