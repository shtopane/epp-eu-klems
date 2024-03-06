# """Tasks running the core analyses."""

from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product, task

from measuring_intangible_capital.config import (
    BLD_PYTHON,
    COUNTRY_CODES,
    DATA_CLEAN_PATH,
)
from measuring_intangible_capital.analysis.intangible_investment import (
    get_country_total_gdp_intangible_investment,
    get_share_of_intangible_investment_per_gdp,
)

share_intangible_of_gdp_deps = {
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

share_intangible_of_gdp_year_ranges = [range(1995, 2007), range(2000, 2005)]

for years in share_intangible_of_gdp_year_ranges:

    @task(id=f"{years.start}_{years.stop - 1}")
    def task_share_intangible_of_gdp(
        years=years,
        depends_on=share_intangible_of_gdp_deps,
        path_to_shares_intangible: Annotated[Path, Product] = BLD_PYTHON / "share_intangible" / f"gdp_aggregate_{years.start}_{years.stop - 1}.pkl",
    ):
        """Calculate share of intangible investment of GDP for a country from 1995 until 2006 and from 2000 to 2004.
        For each country, select the capital and national accounts data
        for the desired years and get the total values for the whole economy(all industries).
        Then calculate the share of intangible investment of GDP for each year and country.
        Store the data frame for each country and concatenate at the end.
        The result is a data frame for all countries with columns: year, country, share_intangible, intangible_gdp.
        Lastly, save the data frame to a pickle file.
        """
        dfs = []

        for index, country_code in enumerate(COUNTRY_CODES):
            capital_accounts = pd.read_pickle(depends_on["capital_accounts"][index])
            national_accounts = pd.read_pickle(depends_on["national_accounts"][index])

            capital_accounts_for_years, national_accounts_for_years = (
                get_country_total_gdp_intangible_investment(
                    capital_accounts=capital_accounts,
                    national_accounts=national_accounts,
                    country_code=country_code,
                    years=years,
                )
            )
            df = get_share_of_intangible_investment_per_gdp(
                capital_accounts_for_years=capital_accounts_for_years,
                national_accounts_for_years=national_accounts_for_years,
            )
            dfs.append(df)

        data_for_plotting = pd.concat(dfs)
        pd.to_pickle(data_for_plotting, path_to_shares_intangible)
