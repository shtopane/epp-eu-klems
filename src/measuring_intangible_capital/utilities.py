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
    if not isinstance(country_code, str):
        raise ValueError("The country code must be a string.")
    
    if country_code not in COUNTRY_CODES:
        raise ValueError(
            f"The country code {country_code} is not valid. Please use one of {COUNTRY_CODES}."
        )
    
    file_names = EU_KLEMS_FILE_NAMES

    if country_code == "SK":
        file_names = [file_name for file_name in file_names if file_name != "growth_accounts"]

    return {
        filename: EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / f"{filename}.xlsx"
        for filename in file_names
    }


def get_percent_of_intangible_sub_components_in_labour_productivity():
    """These are real values from the paper.
    Use the percentages to calculate the share of intangible sub-components in labour productivity
    from total intangible capital deepening.
    Round to 3 decimal points.
    Returns:
        dict[list]: the share of each sub-category of intangible capital(software, R&D, etc) in labour productivity.
        Example:
        {
            "AT": [0.13, 0.29, 0.13], soft_db, innovative_property, economic_competencies
            "DK": [0.29, 0.27, 0.17],
            "CZ": [0.06, 0.35, 0.27],
            "SK": [0.04, 0.07, 0.10],
            "EL": [0.06, 0.11, 0.07],
        }
    """
    # "SK": 0.21,
    intangible_capital_deepening = {
        "AT": 0.55,
        "DK": 0.72,
        "CZ": 0.68,
        "EL": 0.24,
    }

    #  "SK": [0.04, 0.07, 0.10],
    intangible_capital_deepening_by_sub_component = {
        "AT": [0.13, 0.29, 0.13],
        "DK": [0.29, 0.27, 0.17],
        "CZ": [0.06, 0.35, 0.27],
        "EL": [0.06, 0.11, 0.07],
    }

    intangible_capital_deepening_by_sub_component_percentage = {
         country: [round(value / intangible_capital_deepening[country], 3) for value in values]
          for country, values in intangible_capital_deepening_by_sub_component.items()
    }
    
    return intangible_capital_deepening_by_sub_component_percentage