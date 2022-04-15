from helpers.utils import load_calls_correlation_data
import plotly.express as px
from helpers.design import background_color, font_color, font_family

calls = load_calls_correlation_data()


class Data:
    dataframe = {}
    max_size = {}


def types_of_callsbis(freq="M", start=None, end=None, value=None):
    data = Data.dataframe.get(freq)

    if data is None:
        data = calls.loc[start:end]

        data = (
            data.groupby(["desc", 'date'])
            .size()
            .reset_index(0)
            .groupby(["desc"])
            .resample(freq)
            .sum()
            .reset_index(0)
            .rename(columns={0: "number"})
        )

        Data.max_size[freq] = data.number.max()
        Data.dataframe[freq] = data

    data = data.loc[value] if value is not None else data

    fig = px.bar(data, x="desc", y="number", color="desc")


    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        yaxis_range=[0, Data.max_size[freq]],
        showlegend=False,
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    return fig
