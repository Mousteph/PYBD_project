# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
from datetime import date

from figures.correlation_figure import display_correlation_plot
from figures.scatter_figure import display_correlation_scatter
from figures.types_figure import types_of_calls
from figures.type_inout_temp_figure import in_out_of_calls

from helpers.design import background_color, font_color, font_family, color_green
from helpers.utils import load_weather_data


class SliderDataManager:
    def __init__(self):
        yearsM = sorted(load_weather_data().resample("M").mean().index)
        yearsW = sorted(load_weather_data().resample("W").mean().index)
        yearsD = sorted(load_weather_data().resample("D").mean().index)
        self.years = {"M": yearsM, "W": yearsW, "D": yearsD}

        self.range = {}
        self.current_freq = "M"
        self.changed = False

    def get_value(self, value, freq):
        if self.current_freq != freq:
            return self.years.get(freq)[0]

        return self.range.get(value, self.years.get(freq)[0])

    def get_marks(self, freq):
        years = self.years[freq]
        self.range = {i: years[i].strftime("%Y-%m-%d")
                      for i in range(len(years))}
        self.current_freq = freq
        self.changed = True

        marks = {i: "" for i in range(len(years))}

        def create_marks(mark, start, end, prof=3):
            if not prof:
                return

            mid = (start + end) // 2
            mark[mid] = years[mid].strftime("%Y-%m-%d")
            create_marks(mark, start, mid, prof - 1)
            create_marks(mark, mid, end, prof - 1)

        create_marks(marks, 0, len(years))
        marks[len(years) - 1] = years[-1].strftime("%Y-%m-%d")
        marks[0] = years[0].strftime("%Y-%m-%d")

        return len(years) - 1, marks


app = Dash(__name__)
slider_data = SliderDataManager()

frequency = {"Mois": "M", "Semaine": "W", "Jour": "D"}


@app.callback(
    Output("figure-corr", "figure"),
    Input("frequence", "value"),
)
def figure_correlation(freq):
    return display_correlation_plot(frequency.get(freq, "M"))


@ app.callback(
    Output("figure-scatter", "figure"),
    Input("frequence", "value"),
)
def scatter_figure(freq):
    return display_correlation_scatter(frequency.get(freq, "M"))


@ app.callback(
    Output("figure-types", "figure"),
    Output("figure-types-in-out", "figure"),
    Input("frequence", "value"),
    Input("slider", "value"),
)
def figure_types(freq, value):
    freq = frequency.get(freq, "M")
    value = slider_data.get_value(value, freq)

    return (types_of_calls(freq, value=value), in_out_of_calls(freq, value=value))


@ app.callback(
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "marks"),
    Input("frequence", "value"),
)
def slider_years(freq):
    return 0, *slider_data.get_marks(frequency.get(freq, "M"))


@ app.callback(
    Output("slider", "value"),
    Input("slider", "value"),
    Input("stepper", "disabled"),
    Input("stepper", "n_intervals"),
)
def update_slider(value, disable, _):
    if disable:
        return value

    if slider_data.changed:
        slider_data.changed = False
        return 0

    j = len(slider_data.range)
    return 0 if j == 0 else (value + 1) % j


@ app.callback(Output("date-slider", "children"), Input("slider", "value"))
def display_value(value):
    return f"Date : {slider_data.range.get(value)}"


@ app.callback(
    Output("play_pause_button", "children"),
    Output("stepper", "disabled"),
    Input("play_pause_button", "n_clicks"),
    Input("play_pause_button", "children"),
)
def play_pause_button(_, children):
    if children == "Start":
        return "Stop", False

    return "Start", True


paraf = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry.
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
when an unknown printer took a galley of type and scrambled it to make a type specimen book.
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

parafscatter = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry.
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
when an unknown printer took a galley of type and scrambled it to make a type specimen book.
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

paraftype = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry.
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
when an unknown printer took a galley of type and scrambled it to make a type specimen book.
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""

app.layout = html.Div(
    className="app-base",
    children=[
        html.H1("NYPD Calls en fonction de la météo à New York"),
        html.Div(
            className="app-Dropdown-div",
            children=[
                dcc.Dropdown(
                    id="frequence",
                    options=["Jour", "Semaine", "Mois"],
                    value="Mois",
                    searchable=False,
                    clearable=False,
                    persistence=True,
                    className="app-Dropdown",
                ),
            ]
        ),
        html.Div(
            className="graph-div",
            children=[
                html.H2(children="Nombre d'appels et température moyenne"),
                html.Div([dcc.Graph(className="graph", id="figure-corr")]),
                html.P(className="graph-text", children=paraf)
            ]
        ),
        html.Div(
            className="graph-div",
            children=[
                html.H2("Nombre d'appels en fonction de la température moyenne"),
                html.Div([dcc.Graph(className="graph", id="figure-scatter")]),
                html.P(className="graph-text", children=parafscatter),
            ]
        ),
        html.Div(
            [
                html.H2(
                    "Type et lieu des appels par rapport à la température moyenne"
                ),
                html.Div(
                    className="graph-div-types",
                    children=[
                        html.Div(
                            className="graph-types",
                            children=[
                                html.Div(
                                    className="graph-types-general",
                                    children=[dcc.Graph(id="figure-types")],
                                ),
                                html.Div(
                                    className="graph-types-in-out",
                                    children=[
                                        dcc.Graph(id="figure-types-in-out")
                                    ]
                                ),
                            ]
                        ),
                        dcc.Interval(
                            id="stepper",
                            interval=500,  # in milliseconds
                            max_intervals=-1,  # start running
                            n_intervals=0,
                        ),
                        html.Div(
                            id="date-slider",
                            style={
                                "margin": "20px",
                                "text-align": "start",
                                "font-size": "15px",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    html.Button(
                                        children="Start",
                                        id="play_pause_button",
                                        n_clicks=0
                                    ),
                                    style={
                                        "display": "inline-block",
                                        "width": "10%",
                                        "vertical-align": "top",
                                    },
                                ),
                                html.Div(
                                    className="graph-types-slider",
                                    children=dcc.Slider(
                                        id="slider",
                                        value=0,
                                        step=1,
                                    ),
                                ),
                            ],
                        ),
                        html.P(className="graph-text", children=paraf)
                    ]
                ),
            ]
        ),

        html.Div(
            className="graph-div",
            children=[
                html.H2(children="A propos"),
                dcc.Markdown("""
                * Sources :
                   * [Appels NYPD](https://data.cityofnewyork.us/Public-Safety/NYPD-Calls-for-Service-Historic-/d6zx-ckhd) sur data.cityofnewyork.us
                   * [Météo à New-York](https://meteostat.net/fr/place/us/new-york-city?t=2018-01-01/2020-12-31) sur meteostat.net  
                
                * (c) 2022 Moustapha Diop - Mathieu Rivier
                """, style={"text-align": "start"}),
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
