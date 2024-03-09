"""Utilities used in various parts of the project."""

from pathlib import Path
from typing import Literal
import pandas as pd
import yaml

from measuring_intangible_capital.config import (
    ALL_COUNTRIES,
    ALL_COUNTRY_CODES,
    COUNTRIES,
    COUNTRIES_EXTENDED,
    COUNTRY_CODES,
    COUNTRY_CODES_EXTENDED,
    DATA_CLEAN_PATH,
    EU_KLEMS_DATA_DOWNLOAD_PATH,
    EU_KLEMS_FILE_NAMES,
)

ADD_COUNTRY_NAME_MODE = Literal["main", "extended", "all"]

def read_yaml(path):
    """Read a YAML file.

    Args:
        path (str or pathlib.Path): Path to file.

    Returns:
        dict: The parsed YAML file.

    """
    with open(path) as stream:
        try:
            out = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            info = (
                "The YAML file could not be loaded. Please check that the path points "
                "to a valid YAML file."
            )
            raise ValueError(info) from error
    return out


def _add_country_name(df: pd.DataFrame, mode: ADD_COUNTRY_NAME_MODE = "main") -> pd.Series:
    """Add country name to a data frame based on country codes.

    Args:
        df (pd.DataFrame): The data frame.

    Returns:
        pd.Series: The data frame with country name added.

    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The input is not a pandas DataFrame.")

    if "country_code" not in df.columns:
        raise ValueError("The data frame does not contain a column 'country_code'.")

    if df["country_code"].empty:
        return df
    map_dict = dict(zip(COUNTRY_CODES, COUNTRIES))

    if mode == "extended":
        map_dict = dict(zip(COUNTRY_CODES_EXTENDED, COUNTRIES_EXTENDED))
    if mode == "all":
        map_dict = dict(zip(ALL_COUNTRY_CODES, ALL_COUNTRIES))

    return df["country_code"].map(map_dict)

def add_country_name_main_countries(df: pd.DataFrame) -> pd.Series:
    """Add country name to a data frame for the main countries.
    Austria, Czech Republic, Denmark, Greece, and Slovakia.

    Args:
        df (pd.DataFrame): The data frame.

    Returns:
        pd.Series: The data frame with country name added.

    """
    return _add_country_name(df, "main")

def add_country_name_extended_countries(df: pd.DataFrame) -> pd.Series:
    """Add country name to a data frame for the extended countries.
    France, Germany, Italy, Spain, the UK, and the US.

    Args:
        df (pd.DataFrame): The data frame.

    Returns:
        pd.Series: The data frame with country name added.

    """
    return _add_country_name(df, "extended")

def add_country_name_all_countries(df: pd.DataFrame) -> pd.Series:
    """Add country name to a data frame for all countries.

    Args:
        df (pd.DataFrame): The data frame.

    Returns:
        pd.Series: The data frame with country name added.

    """
    return _add_country_name(df, "all")

def get_eu_klems_download_paths(country_code: str) -> dict:
    """Get a dictionary of paths to the EU KLEMS data files for a specific country.
    Structure:
     {filename: path_to_file}, filename is one of the EU_KLEMS_FILE_NAMES.(national_accounts, etc)

    Args:
        country_code (str): the country code for the EU KLEMS data.

    Returns:
        dict: The dictionary of paths to the EU KLEMS data files for each file name(national_accounts, etc).
    """
    if not isinstance(country_code, str):
        raise ValueError("The country code must be a string.")

    if country_code not in ALL_COUNTRY_CODES:
        raise ValueError(
            f"The country code {country_code} is not valid. Please use one of {ALL_COUNTRY_CODES}."
        )

    file_names = EU_KLEMS_FILE_NAMES

    if country_code == "SK":
        file_names = [
            file_name for file_name in file_names if file_name != "growth_accounts"
        ]

    return {
        filename: EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / f"{filename}.xlsx"
        for filename in file_names
    }


def get_account_data_path_for_countries(
    key: Literal["capital", "national", "growth"],
    country_codes: list[str] = ALL_COUNTRY_CODES,
) -> list[Path]:
    paths = [
        Path(DATA_CLEAN_PATH / country_code / f"{key}_accounts.pkl")
        for country_code in country_codes
    ]
    return paths
