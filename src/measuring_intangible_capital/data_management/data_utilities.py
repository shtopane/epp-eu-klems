import pandas as pd


def clean_data(data: pd.DataFrame, data_info: dict) -> pd.DataFrame:
    """Basic cleaning of the data set.
    
    Information on data columns is stored in ``data_management/eu_klems_data_info.yaml``.
    Based on the ``data_info`` object:
    - Drop columns
    - Set categorical columns
    - Rename columns
    - Set index
    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in eu_klems_data_info.yaml.
    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    df = data.drop(columns=data_info["columns_to_drop"])

    for cat_col in data_info["categorical_columns"]:
        df[cat_col] = df[cat_col].astype(pd.CategoricalDtype())
    
    df = df.rename(columns=data_info["column_rename_mapping"])
    
    return df