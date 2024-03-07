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
    get_share_of_tangible_investment_per_gdp,
)

share_tangible_of_gdp_deps = {
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
share_tangible_of_gdp_year_ranges = [[2006], range(2000, 2005)]

for years in share_tangible_of_gdp_year_ranges:
    share_tangible_name = f"{years}" if type(years) == int else f"{years.start}_{years.stop - 1}"

    @task(id=share_tangible_name)
    def task_share_tangible_of_gdp(
        years = years,
        depends_on=share_tangible_of_gdp_deps,
        path_to_shares_tangible: Annotated[Path, Product]= BLD_PYTHON / "share_tangible" / f"gdp_aggregate_{share_tangible_name}.pkl"
    ):
        """Calculate the share of intangible investment of GDP for each country and aggregate category for 2006.
        Each category is: computerized_information, innovative_property, economic_competencies
        """
        dfs = []

        for index, country_code in enumerate(COUNTRY_CODES):
            capital_accounts: pd.DataFrame = pd.read_pickle(depends_on["capital_accounts"][index])
            national_accounts: pd.DataFrame = pd.read_pickle(depends_on["national_accounts"][index])
            
            # For Greece, the investment is under TOT industry code. There's no data on the industry level.
            capital_industry_code = NATIONAL_ACCOUNT_INDUSTRY_CODE if country_code == "EL" else CAPITAL_ACCOUNT_INDUSTRY_CODE
            
            # TODO: Test this is a correct type (pd.DataFrame)
            national_accounts_for_years = national_accounts.loc[NATIONAL_ACCOUNT_INDUSTRY_CODE, years, :]
            national_accounts_for_years = national_accounts_for_years.reset_index(level="industry_code", drop=True)

            capital_accounts_for_years = capital_accounts.loc[capital_industry_code, years, :]
            capital_accounts_for_years = capital_accounts_for_years.reset_index(level="industry_code", drop=True)

            df = get_share_of_tangible_investment_per_gdp(
                capital_accounts=capital_accounts_for_years, 
                national_accounts=national_accounts_for_years,
                country_code=country_code
            )
            dfs.append(df)


        data = pd.concat(dfs)
        
        pd.to_pickle(data, path_to_shares_tangible)
