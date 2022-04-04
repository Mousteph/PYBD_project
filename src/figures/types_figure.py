from helpers.utils import load_calls_correlation_data
import plotly.express as px

calls = load_calls_correlation_data()


def types_of_calls(freq="W", start=None, end=None):
    data = calls.loc[start:end]
    data["types"] = data.TYP_DESC.apply(lambda x: x.split(":")[0])
    data["date"] = data.index

    data = data.groupby(["types", "date"]).size().reset_index(0).groupby(["types"]).resample(
        freq).sum().reset_index().astype({"date": str})

    fig = px.bar(data, y="types", x=0, color="types", animation_frame="date", range_x=[0, data[0].max()])
    fig.update_layout(showlegend=False)

    return fig
