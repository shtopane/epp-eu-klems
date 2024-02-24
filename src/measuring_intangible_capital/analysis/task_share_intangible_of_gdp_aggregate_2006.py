# """Tasks running the core analyses."""

from pathlib import Path
import pandas as pd

from pytask import task

from measuring_intangible_capital.config import (
    BLD,
    COUNTRY_CODES,
    DATA_CLEAN_PATH,
    NATIONAL_ACCOUNT_INDUSTRY_CODE,
)
from measuring_intangible_capital.analysis.intangible_investment import (
    get_country_total_gdp_investment,
    get_intangible_investment_aggregate_types,
    get_share_of_intangible_investment_per_gdp,
)

share_intangible_of_gdp_aggregate_2006_deps = {
    "scripts": [Path("intangible_investment.py")]
}


def task_share_intangible_of_gdp_aggregate_2006(
    depends_on=share_intangible_of_gdp_aggregate_2006_deps,
    path_to_shares_intangible=BLD
    / "python"
    / "share_intangible"
    / "shares_intangible_of_gdp_aggregate_2006.pkl",
):
    """Calculate the share of intangible investment of GDP for each country and aggregate category for 2006.
    Each category is: computerized_information, innovative_property, economic_competencies
    """
    year = 2006
    dfs = []

    for country_code in COUNTRY_CODES:
        capital_accounts = pd.read_pickle(
            DATA_CLEAN_PATH / country_code / "capital_accounts.pkl"
        )
        national_accounts = pd.read_pickle(
            DATA_CLEAN_PATH / country_code / "national_accounts.pkl"
        )

        gdp = (
            national_accounts.loc[NATIONAL_ACCOUNT_INDUSTRY_CODE, year, country_code][
                "gdp"
            ],
        )

        df = get_intangible_investment_aggregate_types(capital_accounts, gdp, year)
        dfs.append(df)

    data = pd.concat(dfs).reset_index()
    pd.to_pickle(data, path_to_shares_intangible)
