"""Task to calculate the composition of labour productivity growth for each country."""

from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product, task

from measuring_intangible_capital.analysis.intangible_investment import (
    get_composition_of_value_added,
)
from measuring_intangible_capital.config import (
    ALL_COUNTRY_CODES_LESS_SK,
    BLD_PYTHON,
    CAPITAL_ACCOUNT_INDUSTRY_CODE,
)
from measuring_intangible_capital.utilities import get_account_data_path_for_countries

labour_productivity_composition_deps = {
    "scripts": [Path("intangible_investment.py")],
    "growth_accounts": get_account_data_path_for_countries(
        "growth",
        ALL_COUNTRY_CODES_LESS_SK,
    ),
}

labour_productivity_composition_year_ranges = [range(1995, 2007)]

for years in labour_productivity_composition_year_ranges:

    @task(id=f"{years.start}_{years.stop - 1}")
    def task_labour_productivity_composition(
        years=years,
        depends_on=labour_productivity_composition_deps,
        path_to_labour_productivity_composition: Annotated[Path, Product] = BLD_PYTHON
        / "labour_productivity"
        / f"composition_{years.start}_{years.stop - 1}.pkl",
    ):
        """Calculate the composition of labour productivity growth for each country.

        For each country, select the growth accounts data for the years 1995 to 2006 and calculate the composition of labour productivity growth.
        Store the data frame for each country and concatenate at the end.
        The result is a data frame for all countries with columns: year, country, composition.
        Lastly, save the data frame to a pickle file.

        """
        dfs = []

        for index, country_code in enumerate(ALL_COUNTRY_CODES_LESS_SK):
            growth_accounts: pd.DataFrame = pd.read_pickle(
                depends_on["growth_accounts"][index],
            )
            growth_accounts_for_years = growth_accounts.loc[
                (CAPITAL_ACCOUNT_INDUSTRY_CODE, list(years), slice(None)),
                :,
            ]

            df = get_composition_of_value_added(growth_accounts_for_years, country_code)
            dfs.append(df)

        labour_productivity_growth_composition = pd.concat(dfs)
        pd.to_pickle(
            labour_productivity_growth_composition,
            path_to_labour_productivity_composition,
        )
