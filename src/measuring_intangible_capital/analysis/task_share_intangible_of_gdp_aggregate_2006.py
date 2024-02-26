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


def task_share_intangible_of_gdp_aggregate_2006(
    depends_on=share_intangible_of_gdp_aggregate_2006_deps,
    path_to_shares_intangible: Annotated[Path, Product] = BLD_PYTHON / "share_intangible" / "gdp_aggregate_2006.pkl",
    path_to_shares_tangible: Annotated[Path, Product]= BLD_PYTHON / "share_tangible" / "gdp_aggregate_2006.pkl"
):
    """Calculate the share of intangible investment of GDP for each country and aggregate category for 2006.
    Each category is: computerized_information, innovative_property, economic_competencies
    """
    year = 2006
    dfs_intangible_investment = []
    dfs_tangible_investment = []
    
    for index, country_code in enumerate(COUNTRY_CODES):
        capital_accounts = pd.read_pickle(depends_on["capital_accounts"][index])
        national_accounts = pd.read_pickle(depends_on["national_accounts"][index])

        gdp = (
            national_accounts.loc[NATIONAL_ACCOUNT_INDUSTRY_CODE, year, country_code][
                "gdp"
            ],
        )

        df_intangible_investment = get_intangible_investment_aggregate_types(
            capital_accounts, gdp, year
        )
        dfs_intangible_investment.append(df_intangible_investment)

        # For Greece, the investment is under TOT industry code. There's no data on the industry level.
        tangible_industry_code = (
            NATIONAL_ACCOUNT_INDUSTRY_CODE
            if country_code == "EL"
            else CAPITAL_ACCOUNT_INDUSTRY_CODE
        )

        df_tangible_investment = get_share_of_tangible_investment_per_gdp(
            capital_accounts, gdp, year, tangible_industry_code
        )
        dfs_tangible_investment.append(df_tangible_investment)

    data_intangible = pd.concat(dfs_intangible_investment).reset_index()
    data_tangible = pd.concat(dfs_tangible_investment).reset_index()

    pd.to_pickle(data_intangible, path_to_shares_intangible)
    pd.to_pickle(data_tangible, path_to_shares_tangible)
