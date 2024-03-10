"""Functions plotting results."""

import math

import pandas as pd
import plotly.express as px

from measuring_intangible_capital.config import (
    COUNTRY_COLOR_MAP,
    COUNTRY_COLOR_MAP_EXTENDED,
    INTANGIBLE_AGGREGATE_CATEGORIES,
    LABOUR_COMPOSITION_COLUMNS_EXTENDED,
    LABOUR_COMPOSITION_PLOT_COLORS,
    PLOT_COLORS_AGGREGATE_CATEGORIES,
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
    return _plot_share_intangibles_for_countries(
        df=df,
        country_color_map=COUNTRY_COLOR_MAP,
        mode="main",
    )


def plot_share_intangibles_for_extended_countries(df: pd.DataFrame):
    """Create Figure 1b: Share Intangible for the extended countries (1995-2006)
    Extended countries are: US, UK, Germany, France, Spain, and Italy.

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    return _plot_share_intangibles_for_countries(
        df=df,
        country_color_map=COUNTRY_COLOR_MAP_EXTENDED,
        mode="extended",
    )


def plot_share_intangible_of_gdp_by_type(df: pd.DataFrame):
    """Create Figure 2: Intangible investment in the market sector (percent of GDP), 2006
    For all countries.

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df = df.reset_index()
    df["country_name"] = add_country_name_all_countries(df)

    df = df.drop("year", axis=1)

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
        color_discrete_sequence=PLOT_COLORS_AGGREGATE_CATEGORIES,
    )

    fig.update_layout(
        _default_fig_layout(
            title="Intangible investment in the market sector (percent of GDP), 2006",
        ),
    )

    return fig


def plot_share_tangible_to_intangible(
    intangible_df: pd.DataFrame,
    tangible_df: pd.DataFrame,
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

    fig.update_layout(
        _default_fig_layout(
            title="Intangible to tangible investment (percent of GDP), 2006",
        ),
    )
    return fig


def plot_composition_of_labour_productivity(df: pd.DataFrame):
    """Create Figure 4a: Contribution of inputs to labour productivity growth, annual average (percent), 1995-2006
    For all countries.

    Args:
        df (pd.DataFrame):  data set containing intangible, labour_composition, tangible_ICT, tangible_nonICT and mfp columns for all countries

    Returns:
       Figure: the plotly figure
    """
    df = df.reset_index()
    df["country_name"] = add_country_name_all_countries(df)

    df_plotting = _data_labour_productivity_bar_chart(
        df=df,
        value_vars=LABOUR_COMPOSITION_COLUMNS_EXTENDED,
    )

    fig = _labour_productivity_bar_chart(
        df=df_plotting,
        color_discrete_sequence=LABOUR_COMPOSITION_PLOT_COLORS,
    )

    fig.update_layout(
        _default_fig_layout(
            title="Contribution of inputs to labour productivity growth, annual average (percent), 1995-2006",
            yaxis_settings={"dtick": 1},
        ),
    )
    return fig


def plot_sub_components_intangible_labour_productivity(df: pd.DataFrame):
    """Create Figure 4b: Contribution of sub-components of intangibles to labour productivity growth, annual
    average (percent), 1995-2006
    For all countries.

    Args:
        df (pd.DataFrame): data set containing computerized_information, innovative_property, economic_competencies, columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df = df.reset_index()
    df["country_name"] = add_country_name_all_countries(df)

    df_plotting = _data_labour_productivity_bar_chart(
        df=df,
        value_vars=INTANGIBLE_AGGREGATE_CATEGORIES,
    )

    fig = _labour_productivity_bar_chart(
        df=df_plotting,
        color_discrete_sequence=PLOT_COLORS_AGGREGATE_CATEGORIES,
    )

    fig.update_layout(
        _default_fig_layout(
            title="Contribution of sub-components of intangibles to labour productivity growth <br> annual average (percent), 1995-2006",
            yaxis_settings={"dtick": 0.2, "range": [-0.2, 1.0]},
        ),
    )
    return fig


def plot_intangible_investment_gdp_per_capita(
    intangible_investment_share: pd.DataFrame,
    gdp_per_capita: pd.DataFrame,
):
    """Create Figure 5a: Intangible investment and GDP per capita (2001-04)
    For all countries
    Args:
        intangible_investment_share (pd.DataFrame): data set containing share_intangible column for all countries
        gdp_per_capita (pd.DataFrame): data set containing gdp_per_capita column for all countries
    Returns:
        Figure: the plotly figure.
    """
    by_country_intangible = intangible_investment_share.groupby(
        level="country_code",
        observed=True,
    )
    by_country_gdp = gdp_per_capita.groupby(level="country_code", observed=True)

    mean_intangible_share: pd.Series = by_country_intangible["share_intangible"].mean()
    mean_gdp_per_capita: pd.Series = by_country_gdp["gdp_per_capita"].mean()

    df = pd.concat([mean_intangible_share, mean_gdp_per_capita], axis=1)
    df = df.reset_index()

    fig = px.scatter(
        df,
        x="gdp_per_capita",
        y="share_intangible",
        color="country_code",
        text="country_code",
    )

    fig.update_traces(_default_diamond_marker())
    fig.update_layout(
        _default_fig_layout(
            title="Intangible investment and GDP per capita (2001-04)",
            show_legend=False,
            yaxis_settings={"range": [0, math.ceil(df["share_intangible"].max())]},
            xaxis_title="GDP per capita (EKS PPP $)",
            yaxis_title="Intangible investment (%GDP)",
        ),
    )

    return fig


def plot_investment_ratio_gdp_per_capita(
    intangible_investment: pd.DataFrame,
    tangible_investment: pd.DataFrame,
    gdp_per_capita: pd.DataFrame,
):
    """Create Figure 5b: Intangible investment ratio and GDP per capita (2001-04)
    For all countries
    Args:
        intangible_investment (pd.DataFrame): data set containing share_intangible column for all countries
        tangible_investment (pd.DataFrame): data set containing share_tangible column for all countries
        gdp_per_capita (pd.DataFrame): data set containing gdp_per_capita column for all countries
    Returns:
        Figure: the plotly figure.
    """
    by_country_intangible = intangible_investment.groupby(
        level="country_code",
        observed=True,
    )
    by_country_tangible = tangible_investment.groupby(
        level="country_code",
        observed=True,
    )
    by_country_gdp = gdp_per_capita.groupby(level="country_code", observed=True)

    mean_gdp_per_capita: pd.Series = by_country_gdp["gdp_per_capita"].mean()

    mean_intangible_share = by_country_intangible["share_intangible"].mean()
    mean_tangible_share = by_country_tangible["share_tangible"].mean()

    mean_ratio: pd.Series = mean_intangible_share / mean_tangible_share
    mean_ratio.name = "intangible_tangible_ratio"

    df = pd.concat([mean_ratio, mean_gdp_per_capita], axis=1)
    df = df.reset_index()

    fig = px.scatter(
        df,
        x="gdp_per_capita",
        y="intangible_tangible_ratio",
        color="country_code",
        text="country_code",
    )

    fig.update_traces(_default_diamond_marker())

    fig.update_layout(
        _default_fig_layout(
            title="Intangible investment ratio and GDP per capita (2001-04)",
            show_legend=False,
            yaxis_settings={
                "range": [0, (df["intangible_tangible_ratio"].max() + 0.1)],
            },
            xaxis_title="GDP per capita (EKS PPP $)",
            yaxis_title="Intangible/tangible investment",
        ),
    )

    return fig


def _default_fig_layout(
    title: str,
    show_legend: bool = True,
    yaxis_settings: dict | None = None,
    xaxis_settings: dict | None = None,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
):
    if xaxis_settings is None:
        xaxis_settings = {}
    if yaxis_settings is None:
        yaxis_settings = {}
    return {
        "title": title,
        "title_x": 0.5,
        "title_font_size": 15,
        "plot_bgcolor": _default_plot_bgcolor(),
        "legend": _default_legend(),
        "showlegend": show_legend,
        "yaxis": dict(_default_yaxis(), **yaxis_settings),
        "xaxis": dict(_default_xaxis(), **xaxis_settings),
        "xaxis_title": xaxis_title,
        "yaxis_title": yaxis_title,
        "autosize": False,
    }


def _default_plot_bgcolor():
    """Return a default plot background color.

    Transparent background.

    """
    return "rgba(0,0,0,0)"


def _default_xaxis():
    """Return a default x-axis layout.

    Show a box around the plot and mirror the axis.

    """
    return {"showline": True, "linewidth": 1, "linecolor": "black", "mirror": True}


def _default_yaxis():
    """Return a default y-axis layout.

    Show only horizontal grid lines. Show a box around the plot and mirror the axis.

    """
    return {
        **_default_xaxis(),
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


def _default_diamond_marker():
    """Makes the data dots in the scatter plot diamond shaped and blue.

    The text is displayed on top of the diamond.

    """
    return {
        "marker": {"symbol": "diamond", "color": "blue"},
        "textposition": "top center",
    }


def _data_labour_productivity_bar_chart(
    df: pd.DataFrame,
    value_vars: list[str],
) -> pd.DataFrame:
    """Prepare the data for the labour productivity bar chart. Melts the data frame by
    country name and the value_vars. assigns a name (component).

    Args:
        df (pd.DataFrame): data set containing intangible, labour_composition, tangible_ICT, tangible_nonICT and mfp columns for all countries
        value_vars (list[str]): the columns to melt

    Returns:
        pd.DataFrame: melted data set

    """
    return df.melt(
        id_vars="country_name",
        value_vars=value_vars,
        var_name="component",
        value_name="value",
    )


def _labour_productivity_bar_chart(
    df: pd.DataFrame,
    color_discrete_sequence: list[str],
):
    """Create a bar chart for the labour productivity composition.

    Args:
        df (pd.DataFrame): data set containing country_name, component, and value columns
        color_discrete_sequence (list[str]): list of colors for the components

    Returns:
        Figure: the plotly figure

    """
    return px.bar(
        df,
        x="country_name",
        y="value",
        color="component",
        color_discrete_sequence=color_discrete_sequence,
    )


def _plot_share_intangibles_for_countries(
    df: pd.DataFrame,
    country_color_map: dict,
    mode: ADD_COUNTRY_NAME_MODE,
):
    """Create Figure 1: Share Intangible for selected countries (1995-2006)
    Get data for all countries and plot the share of intangible investment for the selected countries.

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries.

    Returns:
        Figure: the plotly figure
    """
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

    fig.update_traces(mode="lines+markers", marker={"symbol": "square", "size": 10})

    years = df["year"].unique()
    start_year = years[0]
    end_year = years[-1]

    max_share_intangible = df["share_intangible"].max()

    fig.update_layout(
        _default_fig_layout(
            title=f"Share Intangible for ({start_year}-{end_year})",
            yaxis_settings={"range": [1, math.ceil(max_share_intangible)]},
            xaxis_settings={
                "tickmode": "array",  # Show every year
                "tickvals": years,  # Array of years from the DataFrame
                "showgrid": False,  # No grid for the x-axis
                "title": "Year",
            },
        ),
    )

    return fig
