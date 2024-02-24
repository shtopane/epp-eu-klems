"""Utilities used in various parts of the project."""

import pandas as pd
import yaml

from measuring_intangible_capital.config import COUNTRIES, COUNTRY_CODES


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
    if "country_code" not in df.columns:
        raise ValueError("The data frame does not contain a column 'country_code'.")
    
    return df["country_code"].map(dict(zip(COUNTRY_CODES, COUNTRIES)))