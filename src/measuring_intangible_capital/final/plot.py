"""Functions plotting results."""

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import math

from measuring_intangible_capital.config import (
    COUNTRY_CODES,
    COUNTRY_CODES_EXTENDED,
    COUNTRY_COLOR_MAP,
    COUNTRY_COLOR_MAP_EXTENDED,
    INTANGIBLE_AGGREGATE_CATEGORIES,
    LABOUR_COMPOSITION_COLOR_MAP,
    LABOUR_COMPOSITION_COLUMNS_EXTENDED,
    PLOT_COLORS_BY_COUNTRY,
)
from measuring_intangible_capital.utilities import (
    ADD_COUNTRY_NAME_MODE,
    add_country_name_all_countries,
    add_country_name_extended_countries,
    add_country_name_main_countries,
)


def plot_share_intangibles_for_main_countries(df: pd.DataFrame):
    """Create Figure 1b: Share Intangible for the main countries (1995-2006)
    Main countries are: Austria, Czech Republic, Denmark, Greece, and Slovakia.

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    fig = _plot_share_intangibles_for_countries(
        df=df,
        country_codes=COUNTRY_CODES,
        country_color_map=COUNTRY_COLOR_MAP,
        mode="main",
    )

    return fig


def plot_share_intangibles_for_extended_countries(df: pd.DataFrame):
    """Create Figure 1b: Share Intangible for the extended countries (1995-2006)
    Extended countries are: US, UK, Germany, France, Spain, and Italy.

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    fig = _plot_share_intangibles_for_countries(
        df=df,
        country_codes=COUNTRY_CODES_EXTENDED,
        country_color_map=COUNTRY_COLOR_MAP_EXTENDED,
        mode="extended",
    )

    return fig


def _plot_share_intangibles_for_countries(
    df: pd.DataFrame,
    country_codes: list,
    country_color_map: dict,
    mode: ADD_COUNTRY_NAME_MODE,
):
    """Create Figure 1: Share Intangible for selected countries (1995-2006)

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df = df.loc[(slice(None), country_codes), :]
    df = df.reset_index()

    if mode == "main":
        df["country_name"] = add_country_name_main_countries(df)
    elif mode == "extended":
        df["country_name"] = add_country_name_extended_countries(df)
    else:
        df["country_name"] = add_country_name_all_countries(df)

    fig = px.line(
        df,
        x="year",
        y="share_intangible",
        color="country_name",
        line_group="country_name",
        hover_name="country_name",
        color_discrete_map=country_color_map,
    )

    # Add markers to the line plot
    fig.update_traces(mode="lines+markers", marker=dict(symbol="square", size=10))

    # Get the years from the DataFrame
    years = df["year"].unique()
    start_year = years[0]
    end_year = years[-1]

    max_share_intangible = df["share_intangible"].max()

    fig.update_layout(_default_fig_layout(
        title=f"Share Intangible for All Countries ({start_year}-{end_year})",
        yaxis_settings={"range": [1, math.ceil(max_share_intangible)]},
        ),
        xaxis=dict(
            tickmode="array",  # Show every year
            tickvals=years,  # Array of years from the DataFrame
            showgrid=False,  # No grid for the x-axis
        ),
        xaxis_title="Year",
        )

    return fig


def plot_share_intangible_of_gdp_by_type(df: pd.DataFrame):
    """Create Figure 2: Intangible investment in the market sector (percent of GDP), 2006
    For all countries.

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df = df.reset_index()
    df = df.drop("year", axis=1)
    df["country_name"] = add_country_name_all_countries(df)

    df_melt = df.melt(
        id_vars=["country_name"],
        value_vars=INTANGIBLE_AGGREGATE_CATEGORIES,
        var_name="variable",
        value_name="value",
    )

    fig = px.bar(
        df_melt,
        x="country_name",
        y="value",
        color="variable",
        color_discrete_sequence=PLOT_COLORS_BY_COUNTRY[0:3],
    )

    fig.update_layout(_default_fig_layout(title="Intangible investment in the market sector (percent of GDP), 2006"))

    return fig


def plot_share_tangible_to_intangible(
    intangible_df: pd.DataFrame, tangible_df: pd.DataFrame
):
    """Create Figure 3: Intangible and tangible investment in the market sector (percent of GDP), 2006
    For all countries.

    Args:
        intangible_df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries
        tangible_df (pd.DataFrame): data set containing share_tangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df = pd.concat([intangible_df, tangible_df], axis=1)

    df = df.reset_index()
    df["country_name"] = add_country_name_all_countries(df)

    df_melt = df.melt(
        id_vars="country_name",
        value_vars=["share_intangible", "share_tangible"],
        var_name="variable",
        value_name="value",
    )

    fig = px.bar(
        df_melt,
        x="country_name",
        y="value",
        color="variable",
        barmode="group",
        title="Bar Chart",
        color_discrete_sequence=["lavender", "lightgray"],
    )

    fig.update_layout(_default_fig_layout(title="Intangible to tangible investment (percent of GDP), 2006"))
    return fig


def plot_composition_of_labour_productivity(df: pd.DataFrame):
    """Create Figure 4a: Contribution of inputs to labour productivity growth, annual average (percent), 1995-2006
    For all countries

    Args:
        df (pd.DataFrame):

    Returns:
        _type_: _description_
    """

    df = df.reset_index()
    df["country_name"] = add_country_name_all_countries(df)

    fig = go.Figure(
        data=[
            _get_bar_for_labour_composition(
                df=df,
                column_name=column,
                marker_color=LABOUR_COMPOSITION_COLOR_MAP[column],
            )
            for column in LABOUR_COMPOSITION_COLUMNS_EXTENDED
        ]
    )

    fig.update_layout(
        _default_fig_layout(
            title="Contribution of inputs to labour productivity growth, annual average (percent), 1995-2006",
            yaxis_settings={"dtick": 1},
        ),
        barmode="stack",
    )
    return fig


def plot_sub_components_intangible_labour_productivity(df: pd.DataFrame):
    """Create Figure 4b: Contribution of sub-components of intangibles to labour productivity growth, annual
    average (percent), 1995-2006
    For all countries

    Args:
        df (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    # TODO: Not liking this... refactor or think how to make it better
    df = df.reset_index()

    df["country_name"] = add_country_name_all_countries(df)

    df_melted = df.melt(
        id_vars="country_name",
        value_vars=INTANGIBLE_AGGREGATE_CATEGORIES,
        var_name="component",
        value_name="value",
    )

    fig = px.bar(
        df_melted,
        x="country_name",
        y="value",
        color="component",
        barmode="stack",
        color_discrete_sequence=PLOT_COLORS_BY_COUNTRY[0:3],
    )

    fig.update_layout(
        _default_fig_layout(
            title="Contribution of sub-components of intangibles to labour productivity growth, annual average (percent), 1995-2006",
            yaxis_settings={"dtick": 0.05, "range": [0, 0.5]},
        )
    )
    return fig


def plot_intangible_investment_gdp_per_capita(
    intangible_investment_share: pd.DataFrame, gdp_per_capita: pd.DataFrame
):
    """Create Figure 5a: Intangible investment and GDP per capita (2001-04)"""
    df_share_mean = (
        intangible_investment_share.groupby("country_code")["share_intangible"]
        .mean()
        .reset_index()
    )
    df_gdp_mean = (
        gdp_per_capita.groupby("country_code")["gdp_per_capita"].mean().reset_index()
    )
    df = pd.merge(df_share_mean, df_gdp_mean, on=["country_code"])

    fig = px.scatter(
        df,
        x="gdp_per_capita",
        y="share_intangible",
        color="country_code",
        text="country_code",
        labels={
            "gdp_per_capita": "GDP per capita (EKS PPP $)",
            "share_intangible": "Intangible investment (%GDP)",
        },
    )
    fig.update_traces(
        marker=dict(symbol="diamond", color="blue"), textposition="top center"
    )

    fig.update_layout(
        _default_fig_layout(
            title="Intangible investment and GDP per capita (2001-04)", 
            show_legend=False
        )
    )

    return fig


def plot_investment_ratio_gdp_per_capita(
    intangible_investment: pd.DataFrame,
    tangible_investment: pd.DataFrame,
    gdp_per_capita: pd.DataFrame,
):
    """Create Figure 5b: Intangible investment ratio and GDP per capita (2001-04)"""
    by_country_intangible = intangible_investment.groupby("country_code")
    by_country_tangible = tangible_investment.groupby("country_code")

    mean_ratio = (
        by_country_intangible["share_intangible"].mean()
        / by_country_tangible["share_tangible"].mean()
    )
    mean_gdp = gdp_per_capita.groupby("country_code")["gdp_per_capita"].mean()

    mean_ratio.name = "intangible_tangible_ratio"
    df = pd.merge(mean_ratio, mean_gdp, on=["country_code"])
    df = df.reset_index()

    fig = px.scatter(
        df,
        x="gdp_per_capita",
        y="intangible_tangible_ratio",
        color="country_code",
        text="country_code",
        labels={
            "gdp_per_capita": "GDP per capita (EKS PPP $)",
            "intangible_tangible_ratio": "Intangible/tangible investment",
        },
    )

    fig.update_traces(
        marker=dict(symbol="diamond", color="blue"), textposition="top center"
    )

    fig.update_layout(
        _default_fig_layout(
            title="Intangible investment ratio and GDP per capita (2001-04)",
            show_legend=False,
        )
    )

    return fig


def _default_fig_layout(
    title: str, show_legend: bool = True, yaxis_settings: dict = {}
):
    layout = {
        "title": title,
        "plot_bgcolor": _default_plot_bgcolor(),
        "legend": _default_legend(),
        "showlegend": show_legend,
        "yaxis": dict(_default_yaxis(), **yaxis_settings),
        "xaxis_title": None,
        "yaxis_title": None,
    }

    return layout


def _default_plot_bgcolor():
    """Return a default plot background color.
    Transparent background.
    """
    return "rgba(0,0,0,0)"


def _default_yaxis():
    """Return a default y-axis layout.
    Show only horizontal grid lines.
    """
    return {
        "gridcolor": "gray",  # Only horizontal grid lines
    }


def _default_legend():
    """Return a default legend layout.
    Display the legend horizontally at the bottom of the plot.
    """
    return {
        "title": None,
        "orientation": "h",  # Horizontal orientation
        "yanchor": "top",
        "y": -0.2,  # Adjust this value to move the legend up or down
        "xanchor": "center",
        "x": 0.5,  # Center the legend
    }


def _get_bar_for_labour_composition(
    df: pd.DataFrame, column_name: str, marker_color: str
):
    return go.Bar(
        name=column_name,
        x=df["country_name"],
        y=df[column_name],
        marker_color=marker_color,
    )
