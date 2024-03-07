# """Tasks running the core analyses."""

from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product, task

from measuring_intangible_capital.config import (
    BLD_PYTHON,
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
    COUNTRY_CODES,
    DATA_CLEAN_PATH,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
)
from measuring_intangible_capital.analysis.intangible_investment import (
    get_intangible_investment_aggregate_types,
    get_share_of_tangible_investment_per_gdp,
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
# 2006
# range(2000, 2005)
share_tangible_of_gdp_year_ranges = [2006, range(2000, 2005)]

for years in share_tangible_of_gdp_year_ranges:
    share_tangible_name = str(years) if type(years) == int else f"{years.start}_{years.stop - 1}"

    @task(id=share_tangible_name)
    def task_share_tangible_of_gdp(
        years = years,
        depends_on=share_intangible_of_gdp_aggregate_2006_deps,
        path_to_shares_tangible: Annotated[Path, Product]= BLD_PYTHON / "share_tangible" / f"gdp_aggregate_{share_tangible_name}.pkl"
    ):
        """Calculate the share of intangible investment of GDP for each country and aggregate category for 2006.
        Each category is: computerized_information, innovative_property, economic_competencies
        """
        if isinstance(years, range):
            years = list(years)
        else:
            years = [years]

        dfs_tangible_investment = []

        for index, country_code in enumerate(COUNTRY_CODES):
            capital_accounts: pd.DataFrame = pd.read_pickle(depends_on["capital_accounts"][index])
            national_accounts: pd.DataFrame = pd.read_pickle(depends_on["national_accounts"][index])
            
            # For Greece, the investment is under TOT industry code. There's no data on the industry level.
            capital_industry_code = NATIONAL_ACCOUNT_INDUSTRY_CODE if country_code == "EL" else CAPITAL_ACCOUNT_INDUSTRY_CODE
            
            # TODO: Test this is a correct type (pd.DataFrame)
            national_accounts_for_year = national_accounts.loc[NATIONAL_ACCOUNT_INDUSTRY_CODE, years, :]
            national_accounts_for_year = national_accounts_for_year.reset_index(level="industry_code", drop=True)

            capital_accounts_for_year = capital_accounts.loc[capital_industry_code, years, :]
            capital_accounts_for_year = capital_accounts_for_year.reset_index(level="industry_code", drop=True)

            # print(national_accounts_for_year.index)
            # print(capital_accounts_for_year.index)
        
            df_tangible_investment = get_share_of_tangible_investment_per_gdp(
                capital_accounts=capital_accounts_for_year, 
                national_accounts=national_accounts_for_year,
                country_code=country_code
            )
            print(df_tangible_investment.index)
            print(type(df_tangible_investment))
            dfs_tangible_investment.append(df_tangible_investment)
            # assert False


        data_tangible = pd.concat(dfs_tangible_investment)
        
        pd.to_pickle(data_tangible, path_to_shares_tangible)
