"""Functions plotting results."""

import plotly.express as px

import pandas as pd
import math

from measuring_intangible_capital.config import COUNTRY_COLOR_MAP

def plot_share_intangibles_all_countries(df: pd.DataFrame):
    """Create Figure 1: Share Intangible for All Countries (1995-2006)

    Args:
        df (pd.DataFrame): data set containing share_intangible, year, and country_code columns for all countries

    Returns:
        Figure: the plotly figure
    """
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