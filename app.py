# app.py

from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("moneypuck.csv")
data = pd.melt(data, id_vars=["team", "season", "name", "gameId", "playerTeam", "opposingTeam", "home_or_away", "gameDate", "position", "situation", "date"], var_name="stat")

#data = data.query("situation == 'all'")
#print(data.head())
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Moneypuck Stats"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🏒", className="header_emoji"),
                html.H1(children="Moneypuck Stats Graphed",
                className="header-title"),
                html.P(
                    children="Graphing NHL Team Stats",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Team", className="menu-title"),
                        dcc.Dropdown(
                            id="team-filter",
                            options=[
                                {"label": team, "value": team}
                                for team in np.sort(data.team.unique())
                            ],
                            value="BUF",
                            clearable=False,
                            className="dropdown"
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Season", className="menu-title"),
                        dcc.Dropdown(
                            id="season-filter",
                            options=[
                                {"label": season,
                                "value": season}
                                for season in data.season.unique()
                            ],
                            value=2021,
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Situation", className="menu-title"),
                        dcc.Dropdown(
                            id="situation-filter",
                            options=[
                                {"label": situation,
                                "value": situation}
                                for situation in data.situation.unique()
                            ],
                            value="all",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Stat", className="menu-title"),
                        dcc.Dropdown(
                            id="category-filter",
                            options=[
                                {"label": stat,
                                "value": stat}
                                for stat in data.stat.unique()
                            ],
                            value="xGoalsPercentage",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="xGoalsFor-chart",
                        config={"displayModeBar": False}
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ],
)

@app.callback(
    Output("xGoalsFor-chart", "figure"),
    [ Input("team-filter", "value"), 
    Input("season-filter", "value"),
    Input("situation-filter", "value"),
    Input("category-filter", "value")],
)

def update_charts(team, season, situation, stat):
    mask = (
        (data.team == team)
        & (data.season == season)
        & (data.situation == situation)
        & (data.stat == stat)
    )
    filtered_data = data.loc[mask, :]
    xGoalsFor_chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["value"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "xGoals For Chart",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#3498DB"],
        },
    }
    return xGoalsFor_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)