# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
from datetime import date

from figures.correlation_figure import display_correlation_plot
from figures.scatter_figure import display_correlation_scatter
from figures.types_figure import types_of_calls
from figures.type_inout_temp_figure import in_out_of_calls

from helpers.design import background_color, font_color, font_family
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
        if self.current_freq != freq[0]:
            return self.years.get(freq[0])[0]

        return self.range.get(value, self.years.get(freq[0])[0])

    def get_marks(self, freq):
        years = self.years[freq[0]]
        self.range = {i: years[i].strftime("%Y-%m-%d") for i in range(len(years))}
        self.current_freq = freq[0]
        self.changed = True

        return len(years) - 1, {i: years[i].strftime("%m") for i in range(len(years))}


app = Dash(__name__)
slider_data = SliderDataManager()


@app.callback(
    Output("figure-corr", "figure"),
    Input("frequence-corr", "value"),
    Input("date-picker-range-corr", "start_date"),
    Input("date-picker-range-corr", "end_date"),
)
def figure_correlation(freq, start, end):
    return display_correlation_plot((freq or "Month")[0], start=start, end=end)


@app.callback(
    Output("figure-scatter", "figure"),
    Input("frequence-scatter", "value"),
    Input("date-picker-range-scatter", "start_date"),
    Input("date-picker-range-scatter", "end_date"),
)
def scatter_figure(freq, start, end):
    return display_correlation_scatter((freq or "Month")[0], start=start, end=end)


@app.callback(
    Output("figure-types", "figure"),
    Output("figure-types-in-out", "figure"),
    Input("frequence-types", "value"),
    Input('slider', "value"),
)
def figure_types(freq, value):
    freq = freq or "Month"
    value = slider_data.get_value(value, freq)

    return (types_of_calls(freq[0], value=value),
            in_out_of_calls(freq[0], value=value))

@app.callback(
    Output('slider', "min"),
    Output('slider', "max"),
    Output('slider', "marks"),
    Input("frequence-types", "value"),
)
def slider_years(freq):
    freq = freq or "Month"
    return 0, *slider_data.get_marks(freq)


@app.callback(
    Output('slider', "value"),
    Input("slider", "value"),
    Input("frequence-types", "value"),
    Input('stepper', 'disabled'),
    Input("stepper", "n_intervals"),
)
def update_slider(value, freq, disable, _):
    if disable:
        return value

    if slider_data.changed:
        slider_data.changed = False
        return 0

    j = len(slider_data.range)
    return 0 if j == 0 else (value + 1) % j

@app.callback(
    Output('play_pause_button', 'children'),
    Output('stepper', 'disabled'),
    Input('play_pause_button', 'n_clicks'),
    Input('play_pause_button', 'children'),
)
def play_pause_button(_, children):
    if children == "Play":
        return "Pause", False

    return "Play", True


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
                        options=["Day", "Week", "Month"],
                        value="Month",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                        }
                    ),
                ],
                style={
                    "width": "22%",
                    "margin-right": "20px",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "10%" 
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
                },
            ),

            html.P(paraf, style={"text-align": "justify", "margin-right": "15%", "margin-left": "15%"})

            ],style={
            'justifyContent':'center',
            'text-align': 'center',
            "font-size": "20px",
            "margin-bottom": "90px"}
        ),

        html.Div([
            html.Div(
                [
                    dcc.Graph(id="figure-scatter"),
                ],
                style={
                    "width": "75%",
                    "display": "inline-block",
                    "vertical-align": "top",
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
                        options=["Day", "Week", "Month"],
                        value="Month",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                        }
                    ),
                ],
                style={
                    "width": "22%",
                    "margin-right": "30px",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "margin-top": "10%" 
                },
            ),

            html.P(parafscatter, style={"text-align": "justify", "margin-right": "15%", "margin-left": "15%"})

        ], style={
            'justifyContent':'center',
            'text-align': 'center',
            "font-size": "20px",
            "margin-bottom": "90ppx"
        }),

        html.Div(
            [
                html.Div(
                [
                    dcc.Dropdown(
                        id="frequence-types",
                        options=["Day", "Week", "Month"],
                        value="Month",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "width": "100%",
                        }
                    ),

                    html.Div([
                        html.Div([
                            dcc.Graph(id="figure-types"),
                        ], style={
                            "width": "70%",
                            "height": "100%",
                            "display": "inline-block",
                            "vertical-align": "top",
                        }),

                        html.Div([
                            dcc.Graph(id="figure-types-in-out"),
                        ], style={
                            "width": "30%",
                            "height": "100%",
                            "display": "inline-block",
                            "vertical-align": "top",
                        }),
                        
                    ]),

                    dcc.Interval(
                        id='stepper',
                        interval=1000,       # in milliseconds
                        max_intervals = -1,  # start running
                        n_intervals = 0
                    ),

                    html.Div([
                        dcc.Slider(
                            id='slider',
                            value=0,
                            step = 1,
                        ),

                        html.Button('Play',
                            id='play_pause_button',
                            n_clicks=0,
                            style={'width': '80px', 'height': '60px'}
                        ),
                    ], style={'justifyContent': 'start', 'text-align': 'start'}),
                ],
                style={
                    "width": "90%",
                    "display": "inline-block",
                    "vertical-align": "bottom",
                }),
            ],
            style={
                'justifyContent':'center',
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
