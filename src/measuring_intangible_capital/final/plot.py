"""Functions plotting results."""

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import math

from measuring_intangible_capital.config import COUNTRY_COLOR_MAP, INTANGIBLE_AGGREGATE_CATEGORIES, PLOT_COLORS_BY_COUNTRY
from measuring_intangible_capital.utilities import add_country_name

def plot_share_intangibles_all_countries(df: pd.DataFrame):
    """Create Figure 1: Share Intangible for All Countries (1995-2006)

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df = df.reset_index()

    fig = px.line(
        df,
        x="year",
        y="share_intangible",
        color="country_code",
        line_group="country_code",
        hover_name="country_code",
        color_discrete_map=COUNTRY_COLOR_MAP,
    )

    # Add markers to the line plot
    fig.update_traces(mode="lines+markers", marker=dict(symbol="square", size=10))

    # Get the years from the DataFrame
    years = df["year"].unique()
    start_year = years[0]
    end_year = years[-1]

    # Get the max of share_intangible from the DataFrame
    max_share_intangible = df["share_intangible"].max()

    # Update the layout of the figure
    fig.update_layout(
        title=f"Share Intangible for All Countries ({start_year}-{end_year})",
        xaxis_title="Year",
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        xaxis=dict(
            tickmode="array",  # Show every year
            tickvals=years,  # Array of years from the DataFrame
            showgrid=False,  # No grid for the x-axis
        ),
        yaxis=dict(
            range=[
                1,
                math.ceil(max_share_intangible),
            ],  # Range from 1 to the max of share_intangible
            gridcolor="gray",  # Only horizontal grid lines
        ),
        legend=dict(
            orientation="h",  # Horizontal orientation
            yanchor="top",
            y=-0.2,  # Adjust this value to move the legend up or down
            xanchor="center",
            x=0.5,  # Center the legend
        ),
    )

    return fig

def plot_share_intangible_of_gdp_by_type(df: pd.DataFrame):
    """Create Figure 2: Share Intangible of GDP for All Countries (1995-2006)

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
    df["country_name"] = add_country_name(df)
    df_melt = df.melt(id_vars='country_name', value_vars=INTANGIBLE_AGGREGATE_CATEGORIES, var_name='variable', value_name='value')
    fig = px.bar(df_melt, x='country_name', y='value', color='variable', color_discrete_sequence=PLOT_COLORS_BY_COUNTRY[0:3])

    # Update the layout of the figure
    fig.update_layout(
            title=f"Intangible investment in the market sector (percent of GDP), 2006",
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            legend=dict(
                title=None,
                orientation="h",  # Horizontal orientation
                yanchor="top",
                y=-0.2,  # Adjust this value to move the legend up or down
                xanchor="center",
                x=0.5,  # Center the legend
            ),
            yaxis=dict(
                gridcolor="gray",  # Only horizontal grid lines
            ),
            xaxis_title=None, 
            yaxis_title=None
    )

    return fig

def plot_share_tangible_to_intangible(df: pd.DataFrame):
    df["country_name"] = add_country_name(df)

    df_melt = df.melt(id_vars='country_name', value_vars=['intangible_assets', 'tangible_assets' ], var_name='variable', value_name='value')
    fig = px.bar(df_melt, x='country_name', y='value', color='variable', barmode='group', title='Bar Chart', color_discrete_sequence=['lavender', 'lightgray'])

    fig.update_layout(
                title=f"Intangible to tangible investment (percent of GDP), 2006",
                plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
                legend=dict(
                    title=None,
                    orientation="h",  # Horizontal orientation
                    yanchor="top",
                    y=-0.2,  # Adjust this value to move the legend up or down
                    xanchor="center",
                    x=0.5,  # Center the legend
                ),
                yaxis=dict(
                    gridcolor="gray",  # Only horizontal grid lines
                ),
                xaxis_title=None, 
                yaxis_title=None
        )
    return fig

def plot_composition_of_labour_productivity(df: pd.DataFrame):
    df = df.reset_index()
    df["country_name"] = add_country_name(df)


    columns = [col for col in df.columns if col not in ['country_code', 'country_name', 'labour_productivity']]
    color_map = {
        'intangible': 'royalblue',
        'labour_composition': 'gray',
        'tangible_ICT': 'lightsteelblue',
        'tangible_nonICT': 'darkgray',
        'mfp': 'lavender'
    }

    fig = go.Figure(data=[
        go.Bar(name=column, x=df['country_name'], y=df[column], marker_color=color_map[column]) for column in columns
    ])
    fig.update_layout(
            title="Contribution of inputs to labour productivity growth, annual average (percent), 1995-2006",
            barmode='stack', 
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            legend=dict(
                title=None,
                orientation="h",  # Horizontal orientation
                yanchor="top",
                y=-0.2,  # Adjust this value to move the legend up or down
                xanchor="center",
                x=0.5,  # Center the legend
            ),
            yaxis=dict(
                dtick=1,
                gridcolor="gray",  # Only horizontal grid lines
            ),
            xaxis_title=None, 
            yaxis_title=None
    )
    return fig

def plot_sub_components_intangible_labour_productivity(df: pd.DataFrame):
    # TODO: Not liking this... refactor or think how to make it better
    data_for_plotting = df.copy()

    # Check if the DataFrame has a default index
    if data_for_plotting.index.equals(pd.RangeIndex(start=0, stop=len(df))):
        print("DataFrame has a default index.")
    else:
        print("DataFrame has a custom index. Resetting index.")
        data_for_plotting.reset_index(inplace=True)
    
    data_for_plotting["country_name"] = add_country_name(data_for_plotting)
    
    df_melted = data_for_plotting.melt(id_vars='country_name', value_vars=INTANGIBLE_AGGREGATE_CATEGORIES, var_name='component', value_name='value')

    fig = px.bar(df_melted, x='country_name', y='value', color='component', barmode='stack', color_discrete_sequence=PLOT_COLORS_BY_COUNTRY[0:3])

    fig.update_layout(
            title=f"Contribution of sub-components of intangibles to labour productivity growth, annual average (percent), 1995-2006",
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            legend=dict(
                title=None,
                orientation="h",  # Horizontal orientation
                yanchor="top",
                y=-0.2,  # Adjust this value to move the legend up or down
                xanchor="center",
                x=0.5,  # Center the legend
            ),
            yaxis=dict(
                dtick=0.05, 
                range=[0, 0.5],
                gridcolor="gray",  # Only horizontal grid lines
            ),
            xaxis_title=None, 
            yaxis_title=None
    )
    return fig


def plot_intangible_investment_gdp_per_capita(intangible_investment_share: pd.DataFrame, gdp_per_capita: pd.DataFrame):
    df_share_mean = intangible_investment_share.groupby('country_code')['share_intangible'].mean().reset_index()
    df_gdp_mean = gdp_per_capita.groupby('country_code')['gdp_per_capita'].mean().reset_index()
    df = pd.merge(df_share_mean, df_gdp_mean, on=["country_code"])

    fig = px.scatter(df, x="gdp_per_capita", y="share_intangible", color="country_code", text="country_code",
                 labels={
                     "gdp_per_capita": "GDP per capita (EKS PPP $)",
                     "share_intangible": "Intangible investment (%GDP)"
                 },
                 )
    fig.update_traces(marker=dict(symbol='diamond', color='blue'), textposition='top center')
    fig.update_layout(
            title=f"Intangible investment and GDP per capita (2001-04)",
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            showlegend=False,
            yaxis=dict(
                gridcolor="gray",  # Only horizontal grid lines
            ),
    )

    return fig