from typing import Optional
import pandas as pd


def prepare_accounts(accounts: pd.DataFrame, years: range, industry_code: str, country_code: str = None):
    """Prepare accounts for the analysis.
    We need to select a subset of the accounts: only the intangible assets and the total for all industries.
    Dropping the industry code is done so that calculations between capital accounts and national accounts are straight forward.
    Args:
        accounts (pd.DataFrame): The accounts data set for a given country.
        years (range): The years for which to prepare the data.
        country_code (str): The country code for which to prepare the data.
        industry_code (str): The industry code for which to prepare the data.
    Returns:
        pd.DataFrame: The prepared accounts data set.
    """
    country_code_selector = country_code if country_code else slice(None)

    accounts = accounts.loc[(industry_code, list(years), country_code_selector)]
    accounts = accounts.reset_index(level="industry_code", drop=True)
    return accounts