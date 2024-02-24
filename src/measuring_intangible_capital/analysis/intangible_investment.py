"""Functions to calculate intangible investment."""

import pandas as pd

from measuring_intangible_capital.config import (
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
    DATA_CLEAN_PATH,
    INTANGIBLE_AGGREGATE_CATEGORIES,
    INTANGIBLE_AGGREGATE_CATEGORIES_TYPE,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
)

def _calculate_investment_share_in_gdp(
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

def _aggregate_intangible_investment(df: pd.DataFrame, year: int, mode: INTANGIBLE_AGGREGATE_CATEGORIES_TYPE) -> pd.DataFrame:
    """Aggregate the total market intangible investment data set for a given year.
    Categories are: computerized_information, innovative_property, economic_competencies
    Sum up sub-categories which belong to the aggregate category.
    Ex: computerized_information - software_and_databases, research_and_development
    
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

    data_merged["share_intangible"] = _calculate_investment_share_in_gdp(
        data_merged["investment_level"], data_merged["gdp"]
    )

    # Make year selectable
    data_merged.reset_index(inplace=True)
    return data_merged

def get_intangible_investment_aggregate_types(capital_accounts: pd.DataFrame, gdp: pd.Series, year: int) -> pd.DataFrame:
    """Calculate the share of intangible investment for each aggregate category for a given year.
    For each category, calculate the share of intangible investment of GDP.
    Categories are: computerized_information, innovative_property, economic_competencies

    Args:
        capital_accounts (pd.DataFrame): The capital accounts data set for a given country.
        gdp (pd.Series): The GDP of a given country.
        year (int): The year for which to calculate the share of intangible investment.
    
    Returns:
        pd.DataFrame: The share of intangible investment for each aggregate category.
    """
    df = pd.DataFrame()
     
    for column in INTANGIBLE_AGGREGATE_CATEGORIES:
        df[column] = _calculate_investment_share_in_gdp(
            _aggregate_intangible_investment(capital_accounts, year, column),
            gdp
        )
    return df

def get_share_of_tangible_investment_per_gdp(
        capital_accounts: pd.DataFrame, gdp: pd.Series, year: int,
        industry_code: str = CAPITAL_ACCOUNT_INDUSTRY_CODE
):
    """Calculate the share of tangible investment of GDP for a given year.

    Args:
        capital_accounts (pd.DataFrame): The capital accounts data set for a given country.
        gdp (pd.Series): The GDP of a given country.
        year (int): The year for which to calculate the share of intangible investment.
    
    Returns:
        pd.Series: The share of tangible investment as percent of GDP.
    """
    tangible_assets = capital_accounts.loc[industry_code, year, :]["tangible_assets"]
    
    return _calculate_investment_share_in_gdp(tangible_assets, gdp)
