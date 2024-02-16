"""Function(s) for cleaning the data set(s)."""

import pandas as pd

from measuring_intangible_capital.config import BLD, EU_KLEMS_DATA_DOWNLOAD_PATH, SRC
from measuring_intangible_capital.utilities import read_yaml

def clean_data2(data, data_info):
    """Clean data set.

    Information on data columns is stored in ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'outcome': Name of dependent variable column in data
            - 'outcome_numerical': Name to be given to the numerical version of outcome
            - 'columns_to_drop': Names of columns that are dropped in data cleaning step
            - 'categorical_columns': Names of columns that are converted to categorical
            - 'column_rename_mapping': Old and new names of columns to be renamend,
                stored in a dictionary with design: {'old_name': 'new_name'}
            - 'url': URL to data set

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    data = data.drop(columns=data_info["columns_to_drop"])
    data = data.dropna()
    for cat_col in data_info["categorical_columns"]:
        data[cat_col] = data[cat_col].astype("category")
    data = data.rename(columns=data_info["column_rename_mapping"])

    numerical_outcome = pd.Categorical(data[data_info["outcome"]]).codes
    data[data_info["outcome_numerical"]] = numerical_outcome

    return data


def read_data(data_info: dict, country_code: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """_summary_

    Args:
        data_info (dict): _description_
        country_code (str): _description_

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: _description_
    """
    national_accounts_dfs = []
    capital_accounts_dfs = []

    for sheet in data_info["sheets_to_read"]["capital_accounts"]:
        path_to_file = (
            BLD / EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / "capital_accounts.xlsx"
        )
        data_sheet = pd.read_excel(path_to_file, sheet_name=sheet)
        capital_accounts_dfs.append(data_sheet)

    for sheet in data_info["sheets_to_read"]["national_accounts"]:
        path_to_file = (
            BLD / EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / "national_accounts.xlsx"
        )
        data_sheet = pd.read_excel(path_to_file, sheet_name=sheet)
        national_accounts_dfs.append(data_sheet)

    return capital_accounts_dfs, national_accounts_dfs

def clean_data(data: pd.DataFrame, data_info: dict) -> pd.DataFrame:
    """Clean data set.

    Information on data columns is stored in ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'outcome': Name of dependent variable column in data
            - 'outcome_numerical': Name to be given to the numerical version of outcome
            - 'columns_to_drop': Names of columns that are dropped in data cleaning step
            - 'categorical_columns': Names of columns that are converted to categorical
            - 'column_rename_mapping': Old and new names of columns to be renamend,
                stored in a dictionary with design: {'old_name': 'new_name'}
            - 'url': URL to data set

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    data = data.drop(columns=data_info["columns_to_drop"])
    data = data.dropna()
    for cat_col in data_info["categorical_columns"]:
        data[cat_col] = data[cat_col].astype(pd.CategoricalDtype())
    data = data.rename(columns=data_info["column_rename_mapping"])

    data = data.set_index(["industry_code"])

    return data

def merge_data(data: list[pd.DataFrame], data_info: dict) -> pd.DataFrame:
    """Merge data sets.

    Args:
        data (list[pd.DataFrame]): List of data sets to be merged.

    Returns:
        pd.DataFrame: The merged data set.

    """
    concatenated_pd =  pd.concat(data, axis="rows")

data_info: dict = read_yaml(SRC / "data_management" / "data_info.yaml")
capital_accounts_dfs, national_accounts_dfs = read_data(data_info, "AT")

computers_db_df = clean_data(capital_accounts_dfs[0], data_info)
rd_df = clean_data(capital_accounts_dfs[1], data_info)
other_ipp_assets_df = clean_data(capital_accounts_dfs[2], data_info)
national_accounts_dfs_clean = clean_data(national_accounts_dfs[0], data_info)

concat_intangible = merge_data([rd_df, other_ipp_assets_df], data_info)
print(concat_intangible)
# All industries without public + real estate
industry_code = "MARKT"
print((concat_intangible["2006"].loc[industry_code].sum() /national_accounts_dfs_clean["2006"].max()) * 100)
# print(national_accounts_dfs_clean["2006"].max())

#total_comp_investment_2006 = computers_db_df["2006"].loc[industry_code]
#total_gva_2006 = national_accounts_dfs_clean["2006"].max() #national_accounts_dfs_clean["2006"].loc[industry_code]
#print(f"Share computer software investment AT 2006: {(total_comp_investment_2006 / total_gva_2006) * 100}")
# print(national_accounts_dfs_clean.tail())