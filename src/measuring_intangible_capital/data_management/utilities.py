"""Data management utilities."""
import pandas as pd


def clean_data(raw: pd.DataFrame, data_info: dict) -> pd.DataFrame:
    """Basic cleaning of the data set.

    Information on data columns is stored in ``data_management/eu_klems_data_info.yaml`` and ``data_management/gdp_data_info.yaml``.
    Based on the ``data_info`` object:
    - Drop columns
    - Set categorical columns
    - Rename columns
    - Set index
    Args:
        raw (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in eu_klems_data_info.yaml.

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    df = raw.drop(columns=data_info["columns_to_drop"])

    for categorical_column in data_info["categorical_columns"]:
        df[categorical_column] = df[categorical_column].astype(pd.CategoricalDtype())

    return df.rename(columns=data_info["column_rename_mapping"])
