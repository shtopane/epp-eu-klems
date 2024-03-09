"""Functions to mock data sets for testing purposes."""

import numpy as np
import pandas as pd

from measuring_intangible_capital.config import (
    ALL_COUNTRIES,
    ALL_COUNTRY_CODES_MAP,
    TEST_DIR,
)

MOCK_YEARS_RANGE = range(1995, 1998)
EU_KLEMS_FIXTURE_PATH = TEST_DIR / "data_management" / "eu_klems_data_fixture.xlsx"
GDP_FIXTURE_PATH = TEST_DIR / "data_management" / "gdp_data_fixture.xlsx"


def mock_eu_klems_data():
    """Mock the EU KLEMS data set.
    The data set is a multi-sheet Excel where each variable of interest(say intangible investment) is in a separate sheet.
    In each sheet the variables are: nace_r2_code, geo_code, geo_name, nace_r2_name and then for each year the var values.
    """
    capital_accounts = pd.DataFrame(
        {
            **_get_base_eu_klems_data(),
            "var": ["Capital_Variable", "Capital_Variable", "Capital_Variable"],
        }
    )

    national_accounts = pd.DataFrame(
        {
            **_get_base_eu_klems_data(),
            "var": ["National_Variable", "National_Variable", "National_Variable"],
        }
    )

    growth_accounts = pd.DataFrame(
        {
            **_get_base_eu_klems_data(),
            "var": ["Growth_Variable", "Growth_Variable", "Growth_Variable"],
        }
    )

    return capital_accounts, national_accounts, growth_accounts

def mock_gdp_data():
    """Mock the GDP data set.
    Generate mock data set for all countries.

    """
    gdp = pd.DataFrame(
        {
           **_get_base_gdp_data(),
           **_generate_years_data(
                records=len(ALL_COUNTRIES), min=0.0, max=50_000, column_name=" [YR_TEST]"
            ),
        }
    )

    return gdp

def save_mock_eu_klems_data(capital_accounts, national_accounts, growth_accounts):
    """Save the mock EU KLEMS data set."""
    with pd.ExcelWriter(EU_KLEMS_FIXTURE_PATH, engine="xlsxwriter") as writer:
        capital_accounts.to_excel(writer, sheet_name="Capital_Variable", index=False)
        national_accounts.to_excel(writer, sheet_name="National_Variable", index=False)
        growth_accounts.to_excel(writer, sheet_name="Growth_Variable", index=False)

def save_mock_gdp_data(gdp):
    """Save the mock GDP data set."""
    with pd.ExcelWriter(GDP_FIXTURE_PATH, engine="xlsxwriter") as writer:
        gdp.to_excel(writer, sheet_name="Data", index=False)


def _get_base_eu_klems_data():
    """Get the base data for the mock."""

    base_data = {
        **_generate_years_data(records=3, min=-2000, max=2000),
        "nace_r2_code": ["A", "B", "C"],
        "geo_code": ["AT", "AT", "AT"],
        "geo_name": ["Austria", "Austria", "Austria"],
        "nace_r2_name": ["Agriculture", "Mining", "Manufacturing"],
    }
    return base_data

def _get_base_gdp_data():
    """Generate data for basic columns in the mock GDP data set.
    Series Name, Series Code, Country Code, Country Name.
    The data is junk, except for Country Code and Country Name, 
    which are real and use countries from the project.

    Returns:
        dict: The base data for the mock GDP data set."""
    base_data = {
        "Country Name": ALL_COUNTRIES,
        "Series Name": ["Series Name" for _ in range(len(ALL_COUNTRIES))],
        "Series Code": ["Series Code" for _ in range(len(ALL_COUNTRIES))],
        "Country Code": ALL_COUNTRY_CODES_MAP.keys(),
    }

    return base_data

def _generate_years_data(records: int, min: float, max: float, column_name: str = None):
    """Generate random data for the years in the mock, where each year is a column.
    Args:
        records (int): The number of records to generate.
        min (float): The minimum value for the data.
        max (float): The maximum value for the data.
        column_name (str): Additional string to append to the year number. Default is None.
        If provided, produces column names of the form "2000 [column_name]".
    Returns:
        dict: The data for the years.
        {
            2000: [1, 2, 3],
            2001: [1, 2, 3],
        }
    """
    seed = 92595
    rng = np.random.default_rng(seed=seed)

    result_dict = {}

    for year in MOCK_YEARS_RANGE:
        name = f"{year}{column_name}" if column_name else f"{year}"
        data = min + (max - min) * rng.random(records)
        result_dict[name] = data

    return result_dict
