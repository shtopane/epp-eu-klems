"""Function(s) for cleaning the data set(s)."""

import pandas as pd

from measuring_intangible_capital.config import BLD, COUNTRY_CODES, EU_KLEMS_DATA_DOWNLOAD_PATH, SRC
from measuring_intangible_capital.utilities import read_yaml


def read_data(data_info: dict, country_code: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read investment and national accounts data from the EU KLEMS data set.
    The data is read for a specific country and the sheets specified in the data_info object.

    Args:
        data_info (dict): yaml file with information on the data set.
        country_code (str): AT, CZ, DK, EL, SK

    Returns:
        tuple[list[pd.DataFrame], list[pd.DataFrame]]: list of capital accounts data frames, list of national accounts data frames
    """
    national_accounts_dfs = []
    capital_accounts_dfs = []

    # intangible_analytical_detailed
    # intangible_analytical_aggregate
    for sheet in data_info["sheets_to_read"]["intangible_analytical_detailed"]:
        path_to_file = (
            BLD / EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / "intangible_analytical.xlsx"
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

def clean_and_reshape_eu_klems(
    raw: list[pd.DataFrame], data_info: dict
) -> pd.DataFrame:
    """Clean and reshape the EU KLEMS data set.

    Args:
        raw (pd.DataFrame): The raw data set.
        data_info (dict): Information on data set stored in data_info.yaml.

    Returns:
        pd.DataFrame: The cleaned and reshaped data set.

    """
    data = []

    for df in raw:
        data.append(_clean_data(df, data_info))
    
    data = _concat_eu_klems_data(data)

    years = range(1995, 2020)
    data_merged = _transform_years_columns(data, years)

    data_merged["year"] = data_merged["year"].astype(pd.Int32Dtype())

    data_merged.index = data_merged.index.astype(pd.CategoricalDtype())

    data_merged["investment_type"] = _rename_investment_category(data_merged["investment_type"], data_info["variable_name_mapping"])
    
    data_pivot = data_merged.pivot_table("investment_level", index=["industry_code", "year", "country_code"], columns="investment_type", observed=True)
    data_pivot = data_pivot.round(3)
    # print(f"{50*'-'}Main function{50*'-'}")
    # print(data_pivot)
    return data_pivot

def _clean_data(data: pd.DataFrame, data_info: dict) -> pd.DataFrame:
    """Basic cleaning of the data set.
    
    Information on data columns is stored in ``data_management/data_info.yaml``.
    Based on the ``data_info`` object:
    - Drop columns
    - Set categorical columns
    - Rename columns
    - Set index
    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml.
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


def _concat_eu_klems_data(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatenate all sheets of data into one DataFrame.
    Sets the investment_type column to categorical type.
    Args:
        dfs (list[pd.DataFrame]): The list of data frames to concatenate.
    
    Returns:
        pd.DataFrame: The concatenated data set.
    """
    concatenated = pd.concat(dfs)
    # Category type is not preserved when concatenating dataframes
    # @see https://stackoverflow.com/questions/45639350/retaining-categorical-dtype-upon-dataframe-concatenation
    concatenated["investment_type"] = concatenated["investment_type"].astype(
        pd.CategoricalDtype()
    )

    return concatenated


def _transform_years_columns(
    data: pd.DataFrame, years: range, var_name="year", value_name="investment_level"
) -> pd.DataFrame:
    """Transform the data set from wide to long format based on the years columns.
    The dataset has values under every year column. The returned data set has a year column and the values
    for each each year are stacked under the investment_level column.
    Args:
        data (pd.DataFrame): The data set.
        years (range): years from to range (2000, 2020) for example
        var_name (str, optional): The name of the variable column passed to the ``melt`` method. Defaults to "year".
        value_name (str, optional): The name of the value column passed to the ``melt`` method. Defaults to "investment_level".
    Returns:
        pd.DataFrame: The transformed data set.
    """
    years_as_str = list(map(str, years))

    data = data.melt(
        value_vars=years_as_str,
        value_name=value_name,
        var_name=var_name,
        id_vars=["investment_type", "country_code"],
        ignore_index=False,
    )

    return data

def _rename_investment_category(sr: pd.Series, category_names: dict) -> pd.Series:
    """Rename investment category.

    Args:
        sr (pd.Series): the series to rename
        category_names (dict): category name map in the form of {'old_name': 'new_name'}

    Returns:
        pd.Series: renamed series
    """
    return sr.cat.rename_categories(category_names)

data_info: dict = read_yaml(SRC / "data_management" / "data_info.yaml")
current_country_code = "AT"
industry_code_national_accounts = "TOT"
industry_code_capital_accounts = "MARKT"

#for current_country_code in COUNTRY_CODES:
capital_accounts_dfs, national_accounts_dfs = read_data(data_info, current_country_code)

print(50*"-" + f"Country: {current_country_code}" + 50*"-")

capital_account_df_merged = clean_and_reshape_eu_klems(capital_accounts_dfs, data_info)
national_account_df_merged = clean_and_reshape_eu_klems(national_accounts_dfs, data_info)
print(f"Investment by type 2006: {capital_account_df_merged.loc[industry_code_capital_accounts, 2006, :]}")
# print(national_account_df_merged.loc[industry_code_national_accounts, 2006, current_country_code])
gdp_at_2006 = national_account_df_merged.loc[industry_code_national_accounts, 2006, current_country_code].item()
intangible_investment_at_2006 = capital_account_df_merged.loc[industry_code_capital_accounts, 2006, current_country_code].sum(min_count=1)
print(f"GVA TOT 2006: {gdp_at_2006}")
print(f"Intangible investment 2006: {intangible_investment_at_2006}")
print(f"% of GVA: {round((intangible_investment_at_2006/gdp_at_2006)*100, 2)}")