"""Functions to calculate intangible investment."""

from typing import Literal
import pandas as pd
import plotly.express as px

from measuring_intangible_capital.config import (
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
    COUNTRIES,
    COUNTRY_CODES,
    DATA_CLEAN_PATH,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
    PLOT_COLORS_BY_COUNTRY,
)
from measuring_intangible_capital.final.plot import plot_share_intangible_of_gdp_by_type

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


def get_country_total_gdp_investment(
    country_code: str, years: range
) -> tuple[pd.DataFrame, pd.DataFrame]:
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


def get_share_of_intangible_investment_per_gdp(
    capital_accounts_for_years: pd.DataFrame, national_accounts_for_years: pd.DataFrame
) -> pd.DataFrame:
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

    data_merged["share_intangible"] = _calculate_share_of_intangible_investment(
        data_merged["investment_level"], data_merged["gdp"]
    )

    # Make year selectable
    data_merged.reset_index(inplace=True)
    return data_merged

def aggregate_computerized_information(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Aggregate the intangible investment data set.

    Args:
        df (pd.DataFrame): The intangible investment data set.

    Returns:
        pd.DataFrame: The aggregated intangible investment data set.

    """
    return df.loc[CAPITAL_ACCOUNT_INDUSTRY_CODE, year, :][["software_and_databases", "research_and_development"]].sum(axis=1)

def aggregate_innovative_property(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Aggregate the intangible investment data set.

    Args:
        df (pd.DataFrame): The intangible investment data set.

    Returns:
        pd.DataFrame: The aggregated intangible investment data set.

    """
    return df.loc[CAPITAL_ACCOUNT_INDUSTRY_CODE, year, :][["entertainment_and_artistic", "new_financial_product", "design"]].sum(axis=1)

def aggregate_economic_competencies(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Aggregate the intangible investment data set.

    Args:
        df (pd.DataFrame): The intangible investment data set.

    Returns:
        pd.DataFrame: The aggregated intangible investment data set.

    """
    return df.loc[CAPITAL_ACCOUNT_INDUSTRY_CODE, year, :][["organizational_capital", "brand", "training"]].sum(axis=1)

def aggregate_intangible_investment(df: pd.DataFrame, year: int, mode: Literal['computerized_information', 'innovative_property', 'economic_competencies']) -> pd.DataFrame:
    """Aggregate the intangible investment data set.

    Args:
        df (pd.DataFrame): The intangible investment data set.

    Returns:
        pd.DataFrame: The aggregated intangible investment data set.

    """
    columns = None

    if mode == "computerized_information":
        columns = ["software_and_databases", "research_and_development"]
    elif mode == "innovative_property":
        columns = ["entertainment_and_artistic", "new_financial_product", "design"]
    elif mode == "economic_competencies":
        columns = ["organizational_capital", "brand", "training"]
    else:
        raise ValueError("Invalid mode")
    
    return df.loc[CAPITAL_ACCOUNT_INDUSTRY_CODE, year, :][columns].sum(axis=1)

def get_intangible_investment_aggregate_types(capital_accounts: pd.DataFrame, gdp: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame()
     
    for column in ["computerized_information", "innovative_property", "economic_competencies"]:

        df[column] = _calculate_share_of_intangible_investment(
            aggregate_intangible_investment(capital_accounts, 2006, column),
            gdp
        )
    return df

# dfs = []

# for country_code in COUNTRY_CODES:
#     capital_accounts = pd.read_pickle(DATA_CLEAN_PATH / country_code / "capital_accounts.pkl")
#     national_accounts = pd.read_pickle(DATA_CLEAN_PATH / country_code / "national_accounts.pkl")
    
#     gdp =  national_accounts.loc[NATIONAL_ACCOUNT_INDUSTRY_CODE, 2006, country_code]["gdp"],
    
#     df = get_intangible_investment_aggregate_types(capital_accounts, gdp)
#     dfs.append(df)

# data_plot = pd.concat(dfs).reset_index()
# print(data_plot)

# fig = plot_share_intangible_of_gdp_by_type(data_plot)
# fig.show()
# for country_code in COUNTRY_CODES:
#     capital_accounts_for_years, national_accounts_for_years = get_country_total_gdp_investment(country_code, year_range)
#     data_merged = get_share_of_intangible_investment_per_gdp(capital_accounts_for_years, national_accounts_for_years)
#     dfs_merged.append(data_merged)
