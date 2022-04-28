from helpers.utils import (
    load_calls_correlation_data,
    load_weather_data,
    remove_outliers,
)

from helpers.design import background_color, font_color, font_family, color_blue, color_green

import plotly.express as px

calls = load_calls_correlation_data()
weather = load_weather_data()


def display_correlation_scatter(freq="M"):
    nb_calls = remove_outliers(calls.resample(freq).size())
    tavg = remove_outliers(weather.tavg.resample(freq).mean())
    wspd = remove_outliers(weather.prcp.resample(freq).mean())

    fig = px.scatter(x=tavg, y=nb_calls, trendline="ols", size=wspd,
                     color_discrete_sequence=[color_blue], trendline_color_override=color_green,
                     labels={"x": "température (°C)", "y": "nombre d'appels", "size": "précipitation (mm)"})

    frequency = "mois" if freq == "M" else "semaine" if freq == "W" else "jour"

    fig.update_xaxes(title_text=f"Température moyenne par {frequency}")
    fig.update_yaxes(title_text=f"Nombre d'appels par {frequency}")

    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    return fig
