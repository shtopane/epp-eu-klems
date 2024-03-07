# """Tasks running the core analyses."""

from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product

from measuring_intangible_capital.config import (
    BLD_PYTHON,
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
    COUNTRY_CODES,
    DATA_CLEAN_PATH,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
)
from measuring_intangible_capital.analysis.intangible_investment import (
    get_intangible_investment_aggregate_types,
)

share_intangible_of_gdp_aggregate_2006_deps = {
    "scripts": [Path("intangible_investment.py")],
    "capital_accounts": [
        Path(DATA_CLEAN_PATH / country_code / "capital_accounts.pkl")
        for country_code in COUNTRY_CODES
    ],
    "national_accounts": [
        Path(DATA_CLEAN_PATH / country_code / "national_accounts.pkl")
        for country_code in COUNTRY_CODES
    ],
}

def task_share_intangible_of_gdp_aggregate_2006(
    depends_on=share_intangible_of_gdp_aggregate_2006_deps,
    path_to_shares_intangible: Annotated[Path, Product] = BLD_PYTHON / "share_intangible" / "gdp_aggregate_2006.pkl",
):
    """Calculate the share of intangible investment of GDP for each country and aggregate category for 2006.
    Each category is: computerized_information, innovative_property, economic_competencies
    """
    year = [2006]
    dfs_intangible_investment = []

    for index, country_code in enumerate(COUNTRY_CODES):
        capital_accounts: pd.DataFrame = pd.read_pickle(depends_on["capital_accounts"][index])
        national_accounts: pd.DataFrame = pd.read_pickle(depends_on["national_accounts"][index])
        
         # For Greece, the investment is under TOT industry code. There's no data on the industry level.
        capital_industry_code = NATIONAL_ACCOUNT_INDUSTRY_CODE if country_code == "EL" else CAPITAL_ACCOUNT_INDUSTRY_CODE
        
        # TODO: Test this is a correct type (pd.DataFrame)
        national_accounts_for_year = national_accounts.loc[NATIONAL_ACCOUNT_INDUSTRY_CODE, year, :]
        national_accounts_for_year = national_accounts_for_year.reset_index(level="industry_code", drop=True)
        capital_accounts_for_year = capital_accounts.loc[capital_industry_code, year, :]
        capital_accounts_for_year = capital_accounts_for_year.reset_index(level="industry_code", drop=True)
        
        df_intangible_investment = get_intangible_investment_aggregate_types(
           capital_accounts=capital_accounts_for_year, 
           national_accounts=national_accounts_for_year, 
           country_code=country_code
        )
        df_intangible_investment["intangible_share"] = df_intangible_investment.sum(axis=1)
        dfs_intangible_investment.append(df_intangible_investment)

       
    data_intangible = pd.concat(dfs_intangible_investment)
    
    pd.to_pickle(data_intangible, path_to_shares_intangible)
