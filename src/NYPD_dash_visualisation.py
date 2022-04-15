# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
from datetime import date

from figures.correlation_figure import display_correlation_plot
from figures.scatter_figure import display_correlation_scatter
from figures.types_figure import types_of_callsbis
from figures.type_inout_temp_figure import in_out_of_calls

from helpers.design import background_color, font_color, font_family

from helpers.utils import load_weather_data

weather_data = load_weather_data()

app = Dash(__name__)


@app.callback(
    Output("correlation", "figure"),
    Input("freq", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def correlation_figure(freq, start, end):
    freq = freq or "Month"
    return display_correlation_plot(freq[0], start=start, end=end)


@app.callback(
    Output("scatter", "figure"),
    Input("freq-s", "value"),
    Input("date-picker-range-s", "start_date"),
    Input("date-picker-range-s", "end_date"),
)
def scatter_figure(freq, start, end):
    freq = freq or "Month"
    return display_correlation_scatter(freq[0], start=start, end=end)


class Marks:
    marks = {}
    vals = {"M": "2018-01-31", "W": "2018-01-07", "D": "2018-01-01"}
    current_freq = "M"
    changed = False

@app.callback(
    Output("types", "figure"),
    Input("freq-types", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input('wps-crossfilter-year-slider', "value"),
)
def types_figure(freq, start, end, value):
    freq = freq or "Month"
    if Marks.current_freq != freq[0]:
        value = Marks.vals[freq[0]]
    else:
        value = Marks.marks.get(value, Marks.vals[freq[0]])
    return types_of_callsbis(freq[0], start=start, end=end, value=value)

@app.callback(
    Output('wps-crossfilter-year-slider', "min"),
    Output('wps-crossfilter-year-slider', "max"),
    Output('wps-crossfilter-year-slider', "marks"),
    Input("freq-types", "value"),
)
def slider_years(freq):
    freq = freq or "Month"
    years = sorted(weather_data.tavg.resample(freq[0]).mean().index)
    Marks.marks = {i: years[i].strftime("%Y-%m-%d") for i in range(len(years))}
    Marks.current_freq = freq[0]
    Marks.changed = True
    return 0, len(years) - 1, {i: years[i].strftime("%m") for i in range(len(years))},


@app.callback(
    Output('wps-crossfilter-year-slider', "value"),
    Input("wps-crossfilter-year-slider", "value"),
    Input("wps-auto-stepper", "n_intervals"),
    Input("freq-types", "value"),
    Input('wps-auto-stepper', 'disabled'),
)
def update_slider(value, _, freq, disable):
    if disable:
        return value
        
    if Marks.changed:
        Marks.changed = False
        return 0
    j = len(Marks.marks)
    if j == 0:
        return 0

    return (value + 1) % j

@app.callback(
    Output('play_pause_button', 'children'),
    Output('wps-auto-stepper', 'disabled'),
    Input('play_pause_button', 'n_clicks'),
    Input('play_pause_button', 'children'),
)
def play_pause_button(_, children):
    if children == "Play":
        return "Pause", False

    return "Play", True


# @app.callback(
#     Output("types_in_out", "figure"),
#     Input("freq", "value"),
#     Input("date-picker-range", "start_date"),
#     Input("date-picker-range", "end_date"),
# )
# def types_in_out_figure(freq, start, end):
#     return in_out_of_calls(freq[0], start=start, end=end)


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
                        id="date-picker-range",
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
                        id="freq",
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
                    dcc.Graph(id="correlation"),
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
                    dcc.Graph(id="scatter"),
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
                        id="date-picker-range-s",
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
                        id="freq-s",
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
                        id="freq-types",
                        options=["Day", "Week", "Month"],
                        value="Month",
                        style={
                            "background-color": background_color,
                            "font-color": font_color,
                            "font-family": font_family,
                            "width": "100%",
                        }
                    ),

                    dcc.Graph(id="types"),

                    dcc.Slider(
                        id='wps-crossfilter-year-slider',
                        value=0,
                        step = 1,
                    ),

                    dcc.Interval(
                        id='wps-auto-stepper',
                        interval=1000,       # in milliseconds
                        max_intervals = -1,  # start running
                        n_intervals = 0
                    ),

                    html.Button('Play', id='play_pause_button', n_clicks=0),
                ],
                style={
                    "width": "70%",
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

        #html.Div(
        #    [
        #        dcc.Graph(id="types_in_out"),
        #    ],
        #    style={
        #        "width": "40%",
        #        "display": "inline-block",
        #        "vertical-align": "bottom",
        #    },
        #),
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
