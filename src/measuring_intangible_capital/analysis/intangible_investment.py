"""Functions to calculate intangible investment."""

import warnings
import pandas as pd

from measuring_intangible_capital.config import (
    ALL_COUNTRY_CODES,
    INTANGIBLE_AGGREGATE_CATEGORIES,
    INTANGIBLE_AGGREGATE_CATEGORIES_TYPE,
    INTANGIBLE_DETAIL_CATEGORIES,
    INTANGIBLE_DETAIL_CATEGORIES_TYPE,
    LABOUR_COMPOSITION_COLUMNS,
)
from measuring_intangible_capital.error_handling_utilities import _raise_if_variable_none

def get_share_of_intangible_investment_per_gdp(
    capital_accounts: pd.DataFrame, national_accounts: pd.DataFrame
) -> pd.DataFrame:
    """Calculate investment levels and shares of intangible investment for a country.
    Investment levels are calculated as the sum of intangible assets for all industries.

    Args:
        capital_accounts (pd.DataFrame): data set with investment levels for all industries
        national_accounts (pd.DataFrame): data set with GDP for all industries

    Returns:
        pd.DataFrame: investment levels and shares of intangible investment.
    """
    _raise_if_variable_none(capital_accounts, "capital_accounts")
    _raise_if_variable_none(national_accounts, "national_accounts")
    _raise_data_wrong_type(capital_accounts, "capital_accounts")
    _raise_data_wrong_type(national_accounts, "national_accounts")
    _raise_data_wrong_columns(capital_accounts, INTANGIBLE_DETAIL_CATEGORIES, "capital_accounts")
    _raise_data_wrong_columns(national_accounts, ["gdp"], "national_accounts")

    df = pd.DataFrame()

    df["investment_level"] = capital_accounts[INTANGIBLE_DETAIL_CATEGORIES].sum(axis=1)
    df["share_intangible"] = _calculate_investment_share_in_gdp(
        df["investment_level"], national_accounts["gdp"]
    )

    if (df["share_intangible"] > 100).any():
        warnings.warn("Share of intangible investment is greater than 100% of GDP")

    return df

def get_composition_of_value_added(growth_accounts: pd.DataFrame, country_code: str):
    """Calculate the composition of value added for a given country and industry code.

    Args:
        growth_accounts (pd.DataFrame): The growth accounts data set for a given country.
        country_code (str): The country code for which to calculate the composition of value added.

    Returns:
        pd.DataFrame: The composition of value added.
    """
    _raise_if_variable_none(country_code, "country_code")
    _raise_country_code_wrong_type(country_code)
    _raise_country_code_invalid(country_code)
    _raise_if_variable_none(growth_accounts, "growth_accounts")
    _raise_data_wrong_type(growth_accounts, "growth_accounts")
    _raise_data_wrong_columns(growth_accounts, LABOUR_COMPOSITION_COLUMNS, "growth_accounts")
    
    df = pd.DataFrame(index=pd.Index([country_code], name="country_code"))

    for column in LABOUR_COMPOSITION_COLUMNS:
        df[column] = growth_accounts[column].mean()

    df["labour_productivity"] = growth_accounts["labour_productivity"].mean()
    df["mfp"] = _calculate_mfp(
        labour_productivity=df["labour_productivity"],
        labour_composition=df[LABOUR_COMPOSITION_COLUMNS],
    )

    return df

def get_intangible_investment_aggregate_types(
    capital_accounts: pd.DataFrame, national_accounts: pd.DataFrame, country_code: str
) -> pd.DataFrame:
    """Calculate the share of intangible investment for each aggregate category for a given year.
    For each category, calculate the share of intangible investment of GDP.
    Categories are: computerized_information, innovative_property, economic_competencies

    Args:
        capital_accounts (pd.DataFrame): The capital accounts data set for a given country.
        national_accounts (pd.DataFrame): The national accounts with GDP of a given country.

    Returns:
        pd.DataFrame: The share of intangible investment for each aggregate category.
    """
    _raise_if_index_not_equal(capital_accounts, national_accounts)

    df = pd.DataFrame(
        index=capital_accounts.index, columns=INTANGIBLE_AGGREGATE_CATEGORIES
    )

    gdp = national_accounts.xs(country_code, level="country_code")["gdp"]
    investment = capital_accounts.xs(country_code, level="country_code")

    for category in INTANGIBLE_AGGREGATE_CATEGORIES:
        aggregate_intangible_investment = _aggregate_intangible_investment(
            sr=investment, mode=category
        )

        investment_share = _calculate_investment_share_in_gdp(
            aggregate_intangible_investment,
            gdp,
        )
        investment_share.index = df.index

        df[category] = investment_share

    return df

def get_share_of_tangible_investment_per_gdp(
    capital_accounts: pd.DataFrame, national_accounts: pd.DataFrame, country_code: str
):
    """Calculate the share of tangible investment of GDP for a given year.

    Args:
        capital_accounts (pd.DataFrame): The capital accounts data set for a given industry, year and country.
        national_accounts (pd.DataFrame): The national accounts with GDP of a given industry, year and country.

    Returns:
        pd.Series: The share of tangible investment as percent of GDP.
    """
    _raise_if_index_not_equal(capital_accounts, national_accounts)

    df = pd.DataFrame(index=capital_accounts.index)

    tangible_assets = capital_accounts.xs(country_code, level="country_code")[
        "tangible_assets"
    ]
    gdp = national_accounts.xs(country_code, level="country_code")["gdp"]

    share_tangible = _calculate_investment_share_in_gdp(tangible_assets, gdp)
    share_tangible.index = df.index
    df["share_tangible"] = share_tangible

    return df

def _calculate_mfp(labour_productivity: pd.Series, labour_composition: pd.Series):
    return labour_productivity - labour_composition.sum(axis=1)

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
    sr: pd.Series,
    mode: INTANGIBLE_AGGREGATE_CATEGORIES_TYPE,
) -> pd.Series:
    """Aggregate the total market intangible investment data set for a given year.
    Categories are: computerized_information, innovative_property, economic_competencies
    Sum up sub-categories which belong to the aggregate category.
    Ex: computerized_information - software_and_databases, research_and_development

    Args:
        sr (pd.Series): The total market intangible investment data set for a given year.
        mode (INTANGIBLE_AGGREGATE_CATEGORIES_TYPE): The aggregate category for which to aggregate the data.
            computerized_information: this includes the columns software_and_databases and research_and_development
            innovative_property: this includes the columns entertainment_and_artistic, new_financial_product, design
            economic_competencies: this includes the columns organizational_capital, brand, training
    Returns:
        pd.Series: The aggregate category of intangible investment for a given year.

    """
    _raise_if_variable_none(mode, "mode")
    _raise_aggregate_mode_invalid(mode)

    index: INTANGIBLE_DETAIL_CATEGORIES_TYPE = None

    if mode == "computerized_information":
        index = ["software_and_databases", "research_and_development"]
    elif mode == "innovative_property":
        index = ["entertainment_and_artistic", "new_financial_product", "design"]
    elif mode == "economic_competencies":
        index = ["organizational_capital", "brand", "training"]

    return sr[index].sum(axis=1)

def _raise_if_index_not_equal(
    capital_accounts: pd.DataFrame, national_accounts: pd.DataFrame
):
    if not capital_accounts.index.equals(national_accounts.index):
        raise ValueError("Index is not the same")

def _raise_aggregate_mode_invalid(mode):
    if mode not in INTANGIBLE_AGGREGATE_CATEGORIES:
        raise ValueError("Invalid mode")

def _raise_data_wrong_columns(data, columns: list[str], name: str):
    if not all(column in data.columns for column in columns):
        raise ValueError(f"{name} has the wrong columns")

def _raise_data_wrong_type(data, name):
    if not isinstance(data, pd.DataFrame):
        raise ValueError(f"{name} is not a pandas DataFrame")

def _raise_country_code_invalid(country_code):
    if country_code not in ALL_COUNTRY_CODES:
        raise ValueError(f"Country code {country_code} is not valid")

def _raise_country_code_wrong_type(country_code):
    if not isinstance(country_code, str):
        raise ValueError("country_code is not a string")

