"""Utilities used in various parts of the project."""

import pandas as pd
import yaml

from measuring_intangible_capital.config import (
    COUNTRIES,
    COUNTRY_CODES,
    EU_KLEMS_DATA_DOWNLOAD_PATH,
    EU_KLEMS_FILE_NAMES,
)

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


def add_country_name(df: pd.DataFrame) -> pd.Series:
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
    
    return df["country_code"].map(dict(zip(COUNTRY_CODES, COUNTRIES)))


def get_eu_klems_download_paths(country_code: str) -> dict:
    """Get a dictionary of paths to the EU KLEMS data files for a specific country.
    Structure:
     {filename: path_to_file}, filename is one of the EU_KLEMS_FILE_NAMES.(national_accounts, etc)

    Args:
        country_code (str): the country code for the EU KLEMS data.

    Returns:
        dict: The dictionary of paths to the EU KLEMS data files for each file name(national_accounts, etc).
    """
    return {
        filename: EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / f"{filename}.xlsx"
        for filename in EU_KLEMS_FILE_NAMES
    }
