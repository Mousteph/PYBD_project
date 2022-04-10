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
    fig.update_layout(showlegend=False)

    return fig
