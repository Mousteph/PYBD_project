# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
from datetime import date
from correlation_figure import display_correlation_plot
from scatter_figure import display_correlation_scatter
from types_figure import types_of_calls

app = Dash(__name__)


@app.callback(
    Output('correlation', 'figure'),
    Input('freq', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def correlation_figure(freq, start, end):
    return display_correlation_plot(freq[0], start=start, end=end)


@app.callback(
    Output('scatter', 'figure'),
    Input('freq', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def scatter_figure(freq, start, end):
    return display_correlation_scatter(freq[0], start=start, end=end)


@app.callback(
    Output('types', 'figure'),
    Input('freq', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def types_figure(freq, start, end):
    return types_of_calls(freq[0], start=start, end=end)


app.layout = html.Div([
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=date(2018, 1, 1),
            max_date_allowed=date(2020, 12, 31),
            start_date=date(2018, 1, 1),
            end_date=date(2020, 12, 31)
        ),
        dcc.Dropdown(id='freq', options=['Day', 'Week', 'Month'], value='Month'),
    ], style={'width': '25%', "margin-left": "10px", 'display': 'inline-block',
              "vertical-align": "top", "height": "100%"}),

    html.Div([
        dcc.Graph(
            id='correlation'
        ),
    ], style={'width': '70%', "margin-left": "10px", 'display': 'inline-block',
              "vertical-align": "top", "height": "100%", "border-left": "1px solid black"}),

    html.Div([
        dcc.Graph(
            id='scatter'
        ),
    ], style={'width': '40%', 'display': 'inline-block', "vertical-align": "bottom"}),

    html.Div([
        dcc.Graph(
            id='types'
        ),
    ], style={'width': '60%', 'display': 'inline-block', "vertical-align": "bottom"})
])

if __name__ == '__main__':
    app.run_server(debug=True)
