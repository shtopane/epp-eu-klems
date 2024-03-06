"""Functions to calculate intangible investment."""

import pandas as pd

from measuring_intangible_capital.config import (
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
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


def _aggregate_intangible_investment(
    df: pd.DataFrame,
    year: int,
    mode: INTANGIBLE_AGGREGATE_CATEGORIES_TYPE,
    industry_code: str = CAPITAL_ACCOUNT_INDUSTRY_CODE,
) -> pd.Series:
    """Aggregate the total market intangible investment data set for a given year.
    Categories are: computerized_information, innovative_property, economic_competencies
    Sum up sub-categories which belong to the aggregate category.
    Ex: computerized_information - software_and_databases, research_and_development

    Args:
        df (pd.DataFrame): The intangible investment data set.
        year (int): The year for which to aggregate the data.
        mode (INTANGIBLE_AGGREGATE_CATEGORIES_TYPE): The aggregate category for which to aggregate the data.
            computerized_information: this includes the columns software_and_databases and research_and_development
            innovative_property: this includes the columns entertainment_and_artistic, new_financial_product, design
            economic_competencies: this includes the columns organizational_capital, brand, training
        industry_code (str): The industry code for which to aggregate the data. Default "MARKT".

    Returns:
        pd.Series: The aggregate category of intangible investment for a given year.

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

    return df.loc[industry_code, year, :][columns].sum(axis=1)


def get_country_total_gdp_intangible_investment(
    capital_accounts: pd.DataFrame,
    national_accounts: pd.DataFrame,
    country_code: str,
    years: range,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get totals from capital and national accounts for a country for specific years and industry codes.
    For national accounts - total GDP (VA_CP) is under the industry code "TOT"
    For capital accounts - total of each intangible investment column under the industry code "MARKT"
    Intangible investment are all columns except for "tangible_assets"

    Args:
        capital_accounts (pd.DataFrame): The capital accounts data set for a given country.
        national_accounts (pd.DataFrame): The national accounts data set for a given country.
        country_code (str): For which country to get the data(AT, CZ, DK, EL, SK)
        years (range): for which years to get the data(1995-2006)

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: the sliced capital and national accounts
    """

    capital_accounts_for_years = capital_accounts.loc[
        CAPITAL_ACCOUNT_INDUSTRY_CODE, list(years), country_code
    ]

    # Include only intangible investment columns
    capital_accounts_for_years = capital_accounts_for_years.drop(
        columns="tangible_assets", axis=1
    )

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

def get_composition_of_value_added(
        growth_accounts: pd.DataFrame,
        country_code: str,
        industry_code: str = CAPITAL_ACCOUNT_INDUSTRY_CODE,
):
    """Calculate the composition of value added for a given country and industry code.
    
    Args:
        growth_accounts (pd.DataFrame): The growth accounts data set for a given country.
        country_code (str): The country code for which to calculate the composition of value added.
        industry_code (str): The industry code for which to calculate the composition of value added. Default "MARKT".
    
    Returns:
        pd.DataFrame: The composition of value added.
    """
    df = pd.DataFrame()

    columns = [
        "intangible",
        "labour_composition",
        "tangible_ICT",
        "tangible_nonICT"
    ]

    growth_account_industry = growth_accounts.loc[industry_code, :, :]
    df["country_code"] = [country_code]
    
    for column in columns:
        df[column] = growth_account_industry[column].mean()
    
    df["labour_productivity"] = growth_account_industry["labour_productivity"].mean()
    df["mfp"] = df["labour_productivity"] - df[columns].mean().sum()
    
    return df

def get_intangible_investment_aggregate_types(
    capital_accounts: pd.DataFrame,
    gdp: pd.Series,
    year: int,
    industry_code: str = CAPITAL_ACCOUNT_INDUSTRY_CODE,
) -> pd.DataFrame:
    """Calculate the share of intangible investment for each aggregate category for a given year.
    For each category, calculate the share of intangible investment of GDP.
    Categories are: computerized_information, innovative_property, economic_competencies

    Args:
        capital_accounts (pd.DataFrame): The capital accounts data set for a given country.
        gdp (pd.Series): The GDP of a given country.
        year (int): The year for which to calculate the share of intangible investment.
        industry_code (str): The industry code for which to calculate the share of intangible investment. Typically "MARKT" or "TOT".
        Default "MARKT".

    Returns:
        pd.DataFrame: The share of intangible investment for each aggregate category.
    """
    df = pd.DataFrame()

    for column in INTANGIBLE_AGGREGATE_CATEGORIES:
        aggregate_intangible_investment = _aggregate_intangible_investment(
                capital_accounts, year, column, industry_code
            )
        
        df[column] = _calculate_investment_share_in_gdp(
            aggregate_intangible_investment,
            gdp,
        )
    return df


def get_share_of_tangible_investment_per_gdp(
    capital_accounts: pd.DataFrame,
    gdp: pd.Series,
    year: int,
    industry_code: str = CAPITAL_ACCOUNT_INDUSTRY_CODE,
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
