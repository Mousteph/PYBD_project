from helpers.utils import load_calls_correlation_data
import plotly.express as px


calls = load_calls_correlation_data()

def in_out_of_calls(freq="W", start=None, end=None):
    data = calls.loc[start:end]

    data = (
        data.groupby(["place", 'date'])
        .size()
        .reset_index(0)
        .groupby(["place"])
        .resample(freq)
        .sum()
        .reset_index()
        .astype({"date": str})
        .rename(columns={0: "number"})
    )

    fig = px.bar(
        data,
        y="place",
        x="number",
        color="place",
        animation_frame="date",
        range_x=[0, data["number"].max()],
    )

    fig.update_layout(showlegend=False)

    return fig
