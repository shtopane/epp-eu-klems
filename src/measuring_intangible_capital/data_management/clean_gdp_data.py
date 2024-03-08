"""Functions to clean GDP per capita data from the World Bank."""

from pathlib import Path
import pandas as pd

from measuring_intangible_capital.config import ALL_COUNTRY_CODES, ALL_COUNTRY_CODES_MAP
from measuring_intangible_capital.data_management.utilities import clean_data

def read_data(path: Path, data_info: dict) -> pd.DataFrame:
    """Read the data from the World Bank.
    Read the first N rows for each country in the analysis. End rows are metadata.
    Args:
        data_info (dict): yaml file with information on the data set.

    Returns:
        pd.DataFrame: GDP per capita data
    """
    df = pd.read_excel(
        path, sheet_name=data_info["sheets_to_read"], nrows=len(ALL_COUNTRY_CODES)
    )
    return df


def _rename_year_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename the year columns to only include the year. (2000 [YR2000] -> 2000)
    Args:
      df (pd.DataFrame): The data frame.
    Returns:
      pd.DataFrame: The data frame with the year columns renamed.
    """
    mapper = {col: col.split(" ")[0] for col in df.columns}
    return df.rename(columns=mapper)


def _rename_country_codes(sr: pd.Series) -> pd.Series:
    """Rename the country codes to match our country codes.
    Args:
      df (pd.Series): The column with the country codes.
    Returns:
      pd.Index: The index with the country codes renamed.
    """
    # TODO: Check if this is the right column(entries should be the same length)
    return sr.map(ALL_COUNTRY_CODES_MAP)

def _make_years_separate_column(df: pd.DataFrame) -> pd.DataFrame:
    """Make the years a separate column by melting the data set.
    Args:
      df (pd.DataFrame): The data frame.
    Returns:
      pd.DataFrame: The data frame with the years as a separate column.
    """
    df_melted =  df.melt(id_vars=["country_code"], var_name="year", value_name="gdp_per_capita")
    df_melted["year"] = df_melted["year"].astype(int)
    return df_melted

def clean_gdp_per_capita(raw: pd.DataFrame, data_info: dict):
    df = clean_data(raw, data_info)
    df = _rename_year_columns(df)
    df["country_code"] = _rename_country_codes(df["country_code"])
    df = _make_years_separate_column(df)
    df = df.set_index(["country_code", "year"])

    return df