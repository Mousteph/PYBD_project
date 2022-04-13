from helpers.utils import load_calls_correlation_data
import plotly.express as px

calls = load_calls_correlation_data()


def types_of_calls(freq="W", start=None, end=None):
    data = calls.loc[start:end]

    data = (
        data.groupby(["desc", 'date'])
        .size()
        .reset_index(0)
        .groupby(["desc"])
        .resample(freq)
        .sum()
        .reset_index()
        .astype({"date": str})
        .rename(columns={0: "number"})
    )

    fig = px.bar(data, y="desc", x="number", color="desc", animation_frame="date", range_x=[0, data["number"].max()])

    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        showlegend=False
    )
    return fig


def types_of_callsbis(freq="M", start=None, end=None, value=None):
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

    data = data.loc[value] if value is not None else data

    fig = px.bar(data, x="desc", y="number", color="desc")


    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        showlegend=False
    )

    return fig
