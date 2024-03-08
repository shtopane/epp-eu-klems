from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product, task
from measuring_intangible_capital.analysis.utilities import prepare_accounts

from measuring_intangible_capital.config import (
    ALL_COUNTRY_CODES,
    BLD_PYTHON,
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
)
from measuring_intangible_capital.analysis.intangible_investment import get_share_of_tangible_investment_per_gdp
from measuring_intangible_capital.utilities import get_account_data_path_for_countries

share_tangible_of_gdp_deps = {
    "scripts": [Path("intangible_investment.py")],
    "capital_accounts": get_account_data_path_for_countries("capital"),
    "national_accounts": get_account_data_path_for_countries("national")
}

share_tangible_of_gdp_year_ranges = [[2006], range(2000, 2005)]

for years in share_tangible_of_gdp_year_ranges:
    share_tangible_name = f"{years[0]}" if type(years) == list else f"{years.start}_{years.stop - 1}"

    @task(id=share_tangible_name)
    def task_share_tangible_of_gdp(
        years=years,
        depends_on=share_tangible_of_gdp_deps,
        path_to_shares_tangible: Annotated[Path, Product]= BLD_PYTHON / "share_tangible" / f"gdp_aggregate_{share_tangible_name}.pkl"
    ):
        """Calculate the share of intangible investment of GDP for each country and aggregate category for 2006.
        Each category is: computerized_information, innovative_property, economic_competencies
        """
        dfs = []

        for index, country_code in enumerate(ALL_COUNTRY_CODES):
            capital_accounts: pd.DataFrame = pd.read_pickle(depends_on["capital_accounts"][index])
            national_accounts: pd.DataFrame = pd.read_pickle(depends_on["national_accounts"][index])
            
            # For Greece, the investment is under TOT industry code. There's no data on the industry level.
            capital_industry_code = NATIONAL_ACCOUNT_INDUSTRY_CODE if country_code == "EL" else CAPITAL_ACCOUNT_INDUSTRY_CODE
            
            capital_accounts_for_years = prepare_accounts(
                accounts=capital_accounts,
                years=years,
                industry_code=capital_industry_code,
            )
            national_accounts_for_years = prepare_accounts(
                accounts=national_accounts,
                years=years,
                industry_code=NATIONAL_ACCOUNT_INDUSTRY_CODE,
            )

            df = get_share_of_tangible_investment_per_gdp(
                capital_accounts=capital_accounts_for_years, 
                national_accounts=national_accounts_for_years,
                country_code=country_code
            )
            dfs.append(df)


        data = pd.concat(dfs)
        
        pd.to_pickle(data, path_to_shares_tangible)
