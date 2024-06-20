# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output
from IPython.display import display

# %%
app: Dash = Dash(__name__)
print(__name__)

# %%
# Load the data.
df: pd.DataFrame = pd.read_csv("bees.csv")
display(df.head())

# %%
# Clean the data.
df = df.groupby(["State", "ANSI", "Affected by", "Year", "state_code"])[["Pct of Colonies Impacted"]].mean()
df.reset_index(inplace=True)
display(df.head())

# %%
# App layout
app.layout: html.Div = html.Div([ # type: ignore
    html.H1("Web Application Dashboard with Dash", style={"text-align": "center"}),

    dcc.Dropdown(
        id="slct_year",
        options=[
            {"label": "2015", "value": 2015},
            {"label": "2016", "value": 2016},
            {"label": "2017", "value": 2017},
            {"label": "2018", "value": 2018},
            {"label": "2019", "value": 2019},
        ],
        multi=False,
        value=2015,
        style={"width": "40%"}
    ),

    html.Div(id="output_container", children=[]),
    html.Br(),

    dcc.Graph(id="bee_map", figure={})
])

# %%
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components.
@app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="bee_map", component_property="figure")
    ],
    [Input(component_id="slct_year", component_property="value")]
)
def update_graph(option_slctd: int) -> tuple[str, go.Figure]:
    container: str = f"The year chosen by user is: {option_slctd}"

    df_temp: pd.DataFrame = df.copy()
    df_temp = df_temp[df_temp["Year"] == option_slctd]
    df_temp = df_temp[df_temp["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig: go.Figure = px.choropleth(
        data_frame=df_temp,
        locationmode="USA-states",
        locations="state_code",
        scope="usa",
        color="Pct of Colonies Impacted",
        hover_data=["State", "Pct of Colonies Impacted"],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={"Pct of Colonies Impacted": "% of Bee Colonies"},
        template="plotly_dark"
    )

    # Plotly Graph Objects (GO)
    # fig: go.Figure = go.Figure(
    #     data=[
    #         go.Choropleth(
    #             locationmode="USA-states",
    #             locations=df_temp["state_code"],
    #             z=df_temp["Pct of Colonies Impacted"].astype(float),
    #             colorscale="Reds",
    #             colorbar_title="% of Bee Colonies",
    #         )
    #     ]
    # )
    
    # fig.update_layout(
    #     title_text="Bees Affected by Verroa Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope="usa"),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)