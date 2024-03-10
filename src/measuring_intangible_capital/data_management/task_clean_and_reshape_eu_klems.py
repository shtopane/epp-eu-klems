"""Tasks for cleaning EU KLEMS data."""

from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product, task

from measuring_intangible_capital.config import (
    ALL_COUNTRY_CODES,
    DATA_CLEAN_PATH,
    SRC,
)
from measuring_intangible_capital.data_management.clean_eu_klems_data import (
    clean_and_reshape_eu_klems,
    read_data,
    read_growth_accounts,
)
from measuring_intangible_capital.utilities import (
    get_eu_klems_download_paths,
    read_yaml,
)

clean_data_deps = {
    "scripts": Path("clean_eu_klems_data.py"),
    "data_info": SRC / "data_management" / "eu_klems_data_info.yaml",
}

for country in ALL_COUNTRY_CODES:
    clean_data_deps[f"data_{country}"] = get_eu_klems_download_paths(country)

    @task(id=country)
    def task_clean_and_reshape_eu_klems(
        country: str = country,
        depends_on=clean_data_deps,
        path_to_capital_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH
        / country
        / "capital_accounts.pkl",
        path_to_national_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH
        / country
        / "national_accounts.pkl",
        path_to_growth_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH
        / country
        / "growth_accounts.pkl",
    ):
        """Clean the data (Python version)."""
        data_info = read_yaml(depends_on["data_info"])
        path_to_raw_capital_accounts = Path(
            depends_on[f"data_{country}"]["intangible_analytical"],
        )
        path_to_raw_national_accounts = Path(
            depends_on[f"data_{country}"]["national_accounts"],
        )

        years_for_analysis = range(1995, 2020)

        capital_accounts_raw, national_accounts_raw = read_data(
            data_info=data_info,
            path_to_capital_accounts=path_to_raw_capital_accounts,
            path_to_national_accounts=path_to_raw_national_accounts,
        )

        capital_accounts_clean = clean_and_reshape_eu_klems(
            capital_accounts_raw,
            data_info,
            years=years_for_analysis,
        )
        national_accounts_clean = clean_and_reshape_eu_klems(
            national_accounts_raw,
            data_info,
            years=years_for_analysis,
        )

        capital_accounts_clean.to_pickle(path_to_capital_accounts)
        national_accounts_clean.to_pickle(path_to_national_accounts)

        if country != "SK":
            path_to_raw_growth_accounts = Path(
                depends_on[f"data_{country}"]["growth_accounts"],
            )
            growth_accounts = read_growth_accounts(
                data_info=data_info,
                path_to_growth_accounts=path_to_raw_growth_accounts,
            )
            growth_accounts_clean = clean_and_reshape_eu_klems(
                growth_accounts,
                data_info,
                years=years_for_analysis,
            )
            growth_accounts_clean.to_pickle(path_to_growth_accounts)
        else:
            growth_accounts_clean = pd.DataFrame()
            growth_accounts_clean.to_pickle(path_to_growth_accounts)
