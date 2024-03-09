"""Function(s) for cleaning the EU KLEMS data set(s)."""

from pathlib import Path
import pandas as pd

from measuring_intangible_capital.data_management.utilities import clean_data

def read_data(data_info: dict, path_to_capital_accounts: Path, path_to_national_accounts: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read investment and national accounts data from the EU KLEMS data set.
    The data is read for a specific country and the sheets specified in the data_info object.

    Args:
        data_info (dict): yaml file with information on the data set.
        country_code (str): AT, CZ, DK, EL, SK, UK, US

    Returns:
        tuple[list[pd.DataFrame], list[pd.DataFrame]]: list of capital accounts data frames, list of national accounts data frames
    """
    _raise_data_info_invalid(data_info)
    _raise_keys_not_valid(data_info, ["intangible_analytical_detailed", "national_accounts"])
    _raise_path_invalid(path_to_capital_accounts, "path_to_capital_accounts")
    _raise_path_invalid(path_to_national_accounts, "path_to_national_accounts")

    national_accounts_dfs = []
    capital_accounts_dfs = []
    # BLD / EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / "intangible_analytical.xlsx"
    for sheet in data_info["sheets_to_read"]["intangible_analytical_detailed"]:
        data_sheet = pd.read_excel(path_to_capital_accounts, sheet_name=sheet)
        capital_accounts_dfs.append(data_sheet)

    for sheet in data_info["sheets_to_read"]["national_accounts"]:
        data_sheet = pd.read_excel(path_to_national_accounts, sheet_name=sheet)
        national_accounts_dfs.append(data_sheet)
    
    return capital_accounts_dfs, national_accounts_dfs

def read_growth_accounts(data_info: dict, path_to_growth_accounts: Path) -> list[pd.DataFrame]:
    """Read growth accounts data from the EU KLEMS data set.
    The data is read for a specific country and the sheets specified in the data_info object.

    Args:
        data_info (dict): yaml file with information on the data set.
        country_code (str): AT, CZ, DK, EL

    Returns:
        tuple[list[pd.DataFrame], list[pd.DataFrame]]: list of capital accounts data frames, list of national accounts data frames
    """
    _raise_data_info_invalid(data_info)
    _raise_keys_not_valid(data_info, ["growth_accounts"])
    _raise_path_invalid(path_to_growth_accounts, "path_to_growth_accounts")

    growth_accounts_dfs = []

    for sheet in data_info["sheets_to_read"]["growth_accounts"]:
        data_sheet = pd.read_excel(path_to_growth_accounts, sheet_name=sheet)
        growth_accounts_dfs.append(data_sheet)

    return growth_accounts_dfs

def clean_and_reshape_eu_klems(
    raw: list[pd.DataFrame], data_info: dict
) -> pd.DataFrame:
    """Clean and reshape the EU KLEMS data set.

    Args:
        raw (pd.DataFrame): The raw data set.
        data_info (dict): Information on data set stored in eu_klems_data_info.yaml.

    Returns:
        pd.DataFrame: The cleaned and reshaped data set.

    """
    data = []

    for df in raw:
        data_clean = clean_data(df, data_info)
        data_clean = data_clean.set_index(["industry_code"])
        data.append(data_clean)
    
    df = _concat_eu_klems_data(dfs=data)
    df = _transform_years_columns(df=df, years=range(1995, 2020))

    df["variable_name"] = _rename_variable_category(sr=df["variable_name"], category_names=data_info["variable_name_mapping"])
    df = _pivot_investment_level_to_concrete_investment_categories(df)
    
    return df

def _pivot_investment_level_to_concrete_investment_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot the investment_level column to investment categories as columns.
    Investment categories are the variable_name column.
    Values for the investment categories are the investment_level column.
    Finally, round all values to 3 decimal places.

    The investment categories can be seen in the data_info.yaml file.
    Args:
        df (pd.DataFrame): The data set.
    Returns:
        pd.DataFrame: The pivoted data set.
    """
    df =  df.pivot_table(
        values="investment_level", 
        index=["industry_code", "year", "country_code"], 
        columns="variable_name", 
        observed=True
    )
    df.round(3)

    return df

def _concat_eu_klems_data(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatenate all sheets of data into one DataFrame.
    Sets the variable_name column to categorical type.
    Args:
        dfs (list[pd.DataFrame]): The list of data frames to concatenate.
    
    Returns:
        pd.DataFrame: The concatenated data set.
    """
    concatenated = pd.concat(dfs)
    # Category type is not preserved when concatenating dataframes
    # @see https://stackoverflow.com/questions/45639350/retaining-categorical-dtype-upon-dataframe-concatenation
    concatenated["variable_name"] = concatenated["variable_name"].astype(
        pd.CategoricalDtype()
    )

    return concatenated

def _transform_years_columns(
    df: pd.DataFrame, years: range, var_name="year", value_name="investment_level"
) -> pd.DataFrame:
    """Transform the data set from wide to long format based on the years columns.
    The dataset has values under every year column. The returned data set has a year column and the values
    for each each year are stacked under the investment_level column.
    Args:
        df (pd.DataFrame): The data set.
        years (range): years from to range (2000, 2020) for example
        var_name (str, optional): The name of the variable column passed to the ``melt`` method. Defaults to "year".
        value_name (str, optional): The name of the value column passed to the ``melt`` method. Defaults to "investment_level".
    Returns:
        pd.DataFrame: The transformed data set.
    """
    years_as_str = list(map(str, years))

    df = df.melt(
        value_vars=years_as_str,
        value_name=value_name,
        var_name=var_name,
        id_vars=["variable_name", "country_code"],
        ignore_index=False,
    )

    df["year"] = df["year"].astype(pd.Int16Dtype())

    return df

def _rename_variable_category(sr: pd.Series, category_names: dict) -> pd.Series:
    """Rename variable_name category.
    When we read a data set the variable_name is the name of data set.
    For capital accounts for example we read I_Soft_DB, which is computer software and databases.
    For national accounts we read VA_CP which is value we use as GDP here.
    This function renames this crude names to more descriptive ones.

    The rename dict can be seen in eu_klems_data_info.yaml file.
    ### Aggregate components
    I_Innovprop: intellectual_property
    I_EconComp: economic_competencies
    
    ### Computerized Information
    I_Soft_DB: software_and_databases
    I_RD: research_and_development
    
    ### Intangible Assets national accounts
    I_OIPP: entertainment_and_artistic
    I_NFP: new_financial_product
    I_Design: design

    ### Economic competencies
    I_OrgCap: organizational_capital
    I_Brand: brand
    I_Train: training

    ### National accounts
    VA_CP: gdp

    Args:
        sr (pd.Series): the series to rename
        category_names (dict): category name map in the form of {'old_name': 'new_name'}

    Returns:
        pd.Series: renamed series
    """
    return sr.cat.rename_categories(category_names)

def _raise_path_invalid(path, name: str):
    if not isinstance(path, Path):
        raise TypeError(f"Argument {name} must be a pathlib.Path object.")

def _raise_keys_not_valid(data_info, sheet_names: list[str]):
    if "sheets_to_read" not in data_info:
        raise KeyError("The data_info dictionary must contain the key 'sheets_to_read'.")
    
    for sheet_name in sheet_names:
        if sheet_name not in data_info["sheets_to_read"]:
            raise KeyError(f"The data_info dictionary must contain one of {sheet_names}.")

def _raise_data_info_invalid(data_info):
    if not isinstance(data_info, dict):
        raise TypeError("The data_info argument must be a dictionary.")