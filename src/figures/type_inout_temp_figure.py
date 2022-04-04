from helpers.utils import load_calls_correlation_data
import plotly.express as px

import re

calls = load_calls_correlation_data()


def in_out(line):
    line = line.split("/")[-1]
    inside = ["RESIDENCE", "INSIDE", "DOMESTIC", "COMMERCIAL"]
    outside = ["OUTSIDE", "TRANSIT"]
    if any(ext in line for ext in inside):
        return "INSIDE"
    elif any(ext in line for ext in outside):
        return "OUTSIDE"
    return "UNKNOWNED"


def in_out_of_calls(freq="W", start=None, end=None):
    data = calls.loc[start:end]
    data["types"] = data.TYP_DESC.apply(lambda x: in_out(x))
    print(data["types"].value_counts())
    data["date"] = data.index

    data = (
        data.groupby(["types", "date"])
        .size()
        .reset_index(0)
        .groupby(["types"])
        .resample(freq)
        .sum()
        .reset_index()
        .astype({"date": str})
    )

    fig = px.bar(
        data,
        y="types",
        x=0,
        labels={"types": "endroit", "0": "date"},
        color="types",
        animation_frame="date",
        range_x=[0, data[0].max()],
    )
    fig.update_layout(showlegend=False)

    return fig
