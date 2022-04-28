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

        marks = {
            len(years) - 1: years[-1].strftime("%Y-%m-%d"),
            0: years[0].strftime("%Y-%m-%d"),
        }

        def create_marks(mark, start, end, prof=3):
            if not prof:
                return

            mid = (start + end) // 2
            mark[mid] = years[mid].strftime("%Y-%m-%d")
            create_marks(mark, start, mid, prof - 1)
            create_marks(mark, mid, end, prof - 1)

        create_marks(marks, 0, len(years))

        return len(years) - 1, marks


app = Dash(__name__)
slider_data = SliderDataManager()

frequency = {"Mois": "M", "Semaine": "W", "Jour": "D"}
size_values = {"Précipitations": 0, "Vittesse du vent": 1}


@app.callback(
    Output("figure-corr", "figure"),
    Input("frequence", "value"),
)
def figure_correlation(freq):
    return display_correlation_plot(frequency.get(freq, "M"))


@app.callback(
    Output("figure-scatter", "figure"),
    Input("frequence", "value"),
    Input("size_scatter", "value"),
)
def scatter_figure(freq, size_value):
    return display_correlation_scatter(
        frequency.get(freq, "M"), size_values.get(size_value, 1)
    )


@app.callback(
    Output("figure-types", "figure"),
    Output("figure-types-in-out", "figure"),
    Input("frequence", "value"),
    Input("slider", "value"),
)
def figure_types(freq, value):
    freq = frequency.get(freq, "M")
    value = slider_data.get_value(value, freq)

    return (types_of_calls(freq, value=value), in_out_of_calls(freq, value=value))


@app.callback(
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "marks"),
    Input("frequence", "value"),
)
def slider_years(freq):
    return 0, *slider_data.get_marks(frequency.get(freq, "M"))


@app.callback(
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


@app.callback(Output("date-slider", "children"), Input("slider", "value"))
def display_value(value):
    return f"Date : {slider_data.range.get(value)}"


@app.callback(
    Output("play_pause_button", "children"),
    Output("stepper", "disabled"),
    Input("play_pause_button", "n_clicks"),
    Input("play_pause_button", "children"),
)
def play_pause_button(_, children):
    if children == "Start":
        return "Stop", False

    return "Start", True


paraf_intro = """
Bienvenue,  
Vous pourrez trouver sur cette page des comparaisons et analyses de la corrélation entre la météo
et le nombre d'appels passés au centre d'appel de NYPD à New-York. Chacun des graphes suivants,
permet de mettre en relations différents aspects météorologiques avec le nombre d'appels.  

__Remarque:__  
Grace au bouton ci dessous ___qui est toujours visible sur la page___, vous pourrez changer la
fréquence de tout les graphs de la page.  

Trois options s'offrent à vous:
 - par Mois
 - par Semaine
 - par Jour
"""

paraf_corr = """
Ce graphique représente les courbes de la température moyenne et le nombre d’appels NYPD à New-York
sur une période de 3 ans entre le 1er janvier 2018 et le 31 décembre 2020. On remarque une très forte
corrélation entre les deux courbes. En effet plus la température est élevée, plus le nombre d’appels est
important et inversement plus la température est basse moins le nombre d’appels est élevé.  

__Remarque :__  
Au début de l’année 2020, on remarque une irrégularité au niveau du nombre d’appels. Cela doit être du
à la crise de la Covid-19.
"""

paraf_scatter = """
__À noter__: vous pouvez choisir les données en taille du graphique. Deux options vous sont possibles:
  - Vitesse du vent  
  - Précipitations    

Ce graphique représente le nombre d’appels NYPD en fonction de la température à New-York
sur une période de 3 ans entre le 1er janvier 2018 et le 31 décembre 2020. La taille des bulles correspond
au soit: à la vitesse du vent (par défaut) ou au nombre de millimètre de précipitation. Plus une bulle est grosse, plus il y'a eu du vent/plu.
On remarque que le nombre d’appels est corrélé à la température mais pas corrélé à la précipitation. 
De plus, il est possible de constaté que, au même titre que la précipitation la vitesse du vent, ne semble
pas corrélé avec le nombre d'appels.
En effet les différentes tailles des bulles sont assez uniformément réparties sur l’ensemble du graphique.
"""

paraf_type = """
Ces graphiques représentent le type est le lieu des appels NYPD par rapport à la température à New-York
sur une période de 3 ans entre le 1er janvier 2018 et le 31 décembre 2020. On remarque que le type d’appel
change en fonction de la température mais surtout qu’il y a plus d’appels dans un lieu abrité (intérieur) que 
dans un lieu ouvert (extérieur) quand les températures sont basses et plus d’appels à l’extérieur qu’à l’intérieur
quand les températures sont élevées.
"""

app.layout = html.Div(
    className="app-base",
    children=[
        html.H1("Appels NYPD en fonction de la météo à New-York"),
        html.Div(
            className="app-intro",
            children=[
                dcc.Markdown(paraf_intro, className="paraf_intro"),
            ],
        ),
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
            ],
        ),
        html.Div(
            className="graph-div",
            children=[
                html.H2(children="Nombre d'appels et température moyenne"),
                html.Div([dcc.Graph(className="graph", id="figure-corr")]),
                dcc.Markdown(paraf_corr, className="graph-text"),
            ],
        ),
        html.Div(
            className="graph-div",
            children=[
                html.H2("Nombre d'appels en fonction de la température moyenne"),
                html.Div([dcc.Graph(className="graph", id="figure-scatter")]),
                html.Div(
                    className="app-Dropdown-scatter",
                    children=[
                        dcc.Dropdown(
                            id="size_scatter",
                            options=["Précipitations", "Vitesse du vent"],
                            value="Précipitations",
                            searchable=False,
                            clearable=False,
                            persistence=True,
                            className="app-Dropdown",
                        ),
                    ],
                ),
                dcc.Markdown(paraf_scatter, className="graph-text"),
            ],
        ),
        html.Div(
            [
                html.H2("Type et lieu des appels par rapport à la température moyenne"),
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
                                    children=[dcc.Graph(id="figure-types-in-out")],
                                ),
                            ],
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
                                        n_clicks=0,
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
                        html.P(className="graph-text", children=paraf_type),
                    ],
                ),
            ]
        ),
        html.Div(
            className="graph-div",
            children=[
                html.H2(children="A propos"),
                dcc.Markdown(
                    """
                * Sources :
                   * [Appels NYPD](https://data.cityofnewyork.us/Public-Safety/NYPD-Calls-for-Service-Historic-/d6zx-ckhd) sur data.cityofnewyork.us
                   * [Météo à New-York](https://meteostat.net/fr/place/us/new-york-city?t=2018-01-01/2020-12-31&s=72502) sur meteostat.net  
                """,
                    style={"text-align": "start"},
                ),
            ],
        ),
        html.Footer(
            children=[dcc.Markdown("""(c) 2022 Moustapha Diop - Mathieu Rivier""")]
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
