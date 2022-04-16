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
        self.range = {i: years[i].strftime("%Y-%m-%d") for i in range(len(years))}
        self.current_freq = freq
        self.changed = True

        marks = {i: "" for i in range(len(years))}

        def create_marks(marks, start, end, prof=3):
            if not prof:
                return

            mid = (start + end) // 2
            marks[mid] = years[mid].strftime("%Y-%m-%d")
            create_marks(marks, start, mid, prof - 1)
            create_marks(marks, mid, end, prof - 1)

        create_marks(marks, 0, len(years))
        marks[len(years) - 1] = years[-1].strftime("%Y-%m-%d")
        marks[0] = years[0].strftime("%Y-%m-%d")

        return len(years) - 1, marks


app = Dash(__name__)
slider_data = SliderDataManager()

frequence = {"Mois": "M", "Semaine": "W", "Jour": "D"}


@app.callback(
    Output("figure-corr", "figure"),
    Input("frequence-corr", "value"),
    Input("date-picker-range-corr", "start_date"),
    Input("date-picker-range-corr", "end_date"),
)
def figure_correlation(freq, start, end):
    return display_correlation_plot(frequence.get(freq, "M"), start=start, end=end)


@app.callback(
    Output("figure-scatter", "figure"),
    Input("frequence-scatter", "value"),
    Input("date-picker-range-scatter", "start_date"),
    Input("date-picker-range-scatter", "end_date"),
)
def scatter_figure(freq, start, end):
    return display_correlation_scatter(frequence.get(freq, "M"), start=start, end=end)


@app.callback(
    Output("figure-types", "figure"),
    Output("figure-types-in-out", "figure"),
    Input("frequence-types", "value"),
    Input('slider', "value"),
)
def figure_types(freq, value):
    freq = frequence.get(freq, "M")
    value = slider_data.get_value(value, freq)

    return (types_of_calls(freq, value=value),
            in_out_of_calls(freq, value=value))

@app.callback(
    Output('slider', "min"),
    Output('slider', "max"),
    Output('slider', "marks"),
    Input("frequence-types", "value"),
)
def slider_years(freq):
    return 0, *slider_data.get_marks(frequence.get(freq, "M"))


@app.callback(
    Output('slider', "value"),
    Input("slider", "value"),
    Input('stepper', 'disabled'),
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

@app.callback(
    Output('date-slider', 'children'),
    Input('slider', 'value')
)
def display_value(value):
    return f"Date : {slider_data.range.get(value)}"

@app.callback(
    Output('play_pause_button', 'children'),
    Output('stepper', 'disabled'),
    Input('play_pause_button', 'n_clicks'),
    Input('play_pause_button', 'children'),
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
    [
        html.H1("NYPD Calls en fonction de la météo à New York",
            style={
                "text-align": "center",
                "margin-bottom": "80px",
                "font-size": "50px",
                'font-family': font_family,
                'font-color': font_color,
            }),

        html.Div([
            html.H2("Nombre d'appels et température moyenne",
                style={
                    "text-align": "start",
                    "margin-bottom": "30px",
                    "font-family": font_family,
                    "font-color": font_color,
                }
            ),

            html.Div(
                [
                    dcc.DatePickerRange(
                        id="date-picker-range-corr",
                        min_date_allowed=date(2018, 1, 1),
                        max_date_allowed=date(2020, 12, 31),
                        start_date=date(2018, 1, 1),
                        end_date=date(2020, 12, 31),
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "margin-bottom": "5%",
                        }
                    ),
                    dcc.Dropdown(
                        id="frequence-corr",
                        options=["Jour", "Semaine", "Mois"],
                        value="Mois",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "border-radius": "12px",
                        }
                    ),
                ],
                style={
                    "width": "22%",
                    "margin-right": "20px",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "10%",
                },
            ),

            html.Div(
                [
                    dcc.Graph(id="figure-corr"),
                ],
                style={
                    "width": "75%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "border": f"2px solid lightgrey",
                    "padding": "5px",
                    "border-radius": "12px",
                },
            ),

            html.P(paraf, style={"text-align": "justify", "margin-right": "15%", "margin-left": "15%", "margin-top": "20px"})

            ], style={
            'text-align': 'center',
            "font-size": "20px",
            "margin-bottom": "90px"}
        ),

        html.Div([
            html.H2("Nombre d'appels en fonction de la température moyenne",
                style={
                    "text-align": "start",
                    "margin-bottom": "30px",
                    "font-family": font_family,
                    "font-color": font_color,
                }
            ),

            html.Div(
                [
                    dcc.Graph(id="figure-scatter"),
                ],
                style={
                    "width": "75%",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "border": f"2px solid lightgrey",
                    "padding": "5px",
                    "border-radius": "12px",
                },
            ),

            html.Div(
                [
                    dcc.DatePickerRange(
                        id="date-picker-range-scatter",
                        min_date_allowed=date(2018, 1, 1),
                        max_date_allowed=date(2020, 12, 31),
                        start_date=date(2018, 1, 1),
                        end_date=date(2020, 12, 31),
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "margin-bottom": "5%",
                        }
                    ),
                    dcc.Dropdown(
                        id="frequence-scatter",
                        options=["Jour", "Semaine", "Mois"],
                        value="Mois",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "border-radius": "12px",
                        }
                    ),
                ],
                style={
                    "width": "22%",
                    "margin-left": "20px",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "10%" 
                },
            ),

            html.P(parafscatter, style={"text-align": "justify", "margin-right": "15%",
                "margin-left": "15%", "margin-top": "20px"})

        ], style={
            'text-align': 'center',
            "font-size": "20px",
            "margin-bottom": "90ppx"
        }),

        html.Div(
            [
                html.H2("Type et lieu des appels par rapport à la température moyenne",
                    style={
                        "text-align": "start",
                        "margin-bottom": "30px",
                        "font-family": font_family,
                        "font-color": font_color,
                    }
                ),

                html.Div(
                [
                    dcc.Dropdown(
                        id="frequence-types",
                        options=["Jour", "Semaine", "Mois"],
                        value="Mois",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "border-radius": "12px",
                            "margin-bottom": "20px",
                        }
                    ),

                    html.Div([
                        html.Div([
                            dcc.Graph(id="figure-types"),
                        ], style={
                            "width": "70%",
                            "display": "inline-block",
                            "vertical-align": "top",
                        }),

                        html.Div([
                            dcc.Graph(id="figure-types-in-out"),
                        ], style={
                            "width": "30%",
                            "display": "inline-block",
                            "vertical-align": "top",
                        }),
                        
                    ], style={"border": f"2px solid lightgrey", "padding": "5px", "border-radius": "12px",}),

                    dcc.Interval(
                        id='stepper',
                        interval=1000,       # in milliseconds
                        max_intervals = -1,  # start running
                        n_intervals = 0
                    ),

                    html.Div(id='date-slider', style={'margin': "20px", 'text-align': 'start', "font-size": "15px"}),

                    html.Div([
                        html.Div(
                            html.Button('Start',
                                id='play_pause_button',
                                n_clicks=0,
                                style={
                                    'width': '55px',
                                    'height': '35px',
                                    "background-color": color_green,
                                    "border-radius": "12px",
                                    "border": "none",
                                    "color": "white",
                                    "font-size": "15px",
                                    "font-family": font_family,
                                }
                            ),
                            style={"display": "inline-block", "width": "10%", "vertical-align": "top"}
                        ),

                        html.Div(
                            dcc.Slider(
                                id='slider',
                                value=0,
                                step = 1,
                            ),
                            style={"display": "inline-block", "width": "85%", "vertical-align": "top"}
                        ),
                        
                    ],),
                ],
                style={
                    "width": "90%",
                    "display": "inline-block",
                }),

                html.P(paraf, style={
                    "text-align": "justify",
                    "margin-right": "15%",
                    "margin-left": "15%",
                    "margin-top": "50px",}),
            ],
            style={
                'text-align': 'center',
                "font-size": "20px",
                "margin-top": "90px"
            }
        )
    ],
    style={
        "padding": "4%",
        "background-color": background_color,
        "font-color": font_color,
        "font-family": font_family
        },
)


if __name__ == "__main__":
    app.run_server(debug=True)
