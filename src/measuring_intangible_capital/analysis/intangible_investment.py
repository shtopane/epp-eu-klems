"""Functions to calculate intangible investment."""

import numpy as np
import pandas as pd
import math
import plotly.express as px

import plotly.graph_objects as go
from measuring_intangible_capital.config import (
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
    COUNTRY_CODES,
    COUNTRY_COLOR_MAP,
    DATA_CLEAN_PATH,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
)

def _calculate_share_of_intangible_investment(
    intangible_investment: pd.Series, gdp: pd.Series
) -> pd.Series:
    """Calculate intangible investment.

    Args:
        capital_accounts (pandas.DataFrame): Capital accounts data set.
        national_accounts (pandas.DataFrame): National accounts data set.

    Returns:
        pandas.DataFrame: The intangible investment data set.

    """
    return round((intangible_investment / gdp) * 100, 3)

def get_country_total_gdp_investment(country_code: str, years: range) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get totals from capital and national accounts for a country for specific years and industry codes.
    For national accounts - total GDP (VA_CP) is under the industry code "TOT"
    For capital accounts - total of each investment column is under the industry code "MARKT"

    Args:
        country_code (str): For which country to get the data(AT, CZ, DK, EL, SK)
        years (range): for which years to get the data(1995-2006)

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: the sliced capital and national accounts
    """
    capital_accounts: pd.DataFrame = pd.read_pickle(
        DATA_CLEAN_PATH / country_code / "capital_accounts.pkl"
    )
    national_accounts: pd.DataFrame = pd.read_pickle(
        DATA_CLEAN_PATH / country_code / "national_accounts.pkl"
    )

    capital_accounts_for_years = capital_accounts.loc[
        CAPITAL_ACCOUNT_INDUSTRY_CODE, list(years), country_code
    ]
    national_accounts_for_years = national_accounts.loc[
        NATIONAL_ACCOUNT_INDUSTRY_CODE, list(years), country_code
    ]

    return capital_accounts_for_years, national_accounts_for_years

def get_share_of_intangible_investment_per_gdp(capital_accounts_for_years: pd.DataFrame, national_accounts_for_years: pd.DataFrame) -> pd.DataFrame:
    """Calculate investment levels and shares of intangible investment for a country.
    Merge with a country GDP data set.

    Args:
        capital_accounts_for_years (pd.DataFrame): _description_
        national_accounts_for_years (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: the merged data set(investment data and GDP data)
    """

    df = pd.DataFrame()
    df["investment_level"] = capital_accounts_for_years.sum(axis=1)

    data_merged = pd.merge(
        df, national_accounts_for_years, on=["year", "country_code"], how="inner"
    )

    # TODO: Rename in data cleaning stage?
    data_merged = data_merged.rename(columns={"VA_CP": "GDP"})

    data_merged["share_intangible"] = _calculate_share_of_intangible_investment(
        data_merged["investment_level"], data_merged["GDP"]
    )
    data_merged.reset_index(inplace=True)
    return data_merged

year_range = range(1995, 2007)

dfs_merged = []

for country_code in COUNTRY_CODES:
    capital_accounts_for_years, national_accounts_for_years = get_country_total_gdp_investment(country_code, year_range)
    data_merged = get_share_of_intangible_investment_per_gdp(capital_accounts_for_years, national_accounts_for_years)
    dfs_merged.append(data_merged)

