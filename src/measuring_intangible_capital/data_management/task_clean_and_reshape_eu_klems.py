"""Tasks for managing the data."""

from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product, task

from measuring_intangible_capital.config import (
    COUNTRY_CODES,
    DATA_CLEAN_PATH,
    SRC,
)
from measuring_intangible_capital.utilities import (
    get_eu_klems_download_paths,
    read_yaml,
)
from measuring_intangible_capital.data_management.clean_data import (
    read_data,
    clean_and_reshape_eu_klems,
    read_growth_accounts,
)

clean_data_deps = {
    "scripts": Path("clean_data.py"),
    "data_info": SRC / "data_management" / "eu_klems_data_info.yaml",
}

for country in COUNTRY_CODES:
    clean_data_deps[f"data_{country}"] = get_eu_klems_download_paths(country)

    @task(id=country)
    def task_clean_and_reshape_eu_klems(
        country: str = country,
        depends_on=clean_data_deps,
        path_to_capital_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH / country / "capital_accounts.pkl",
        path_to_national_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH / country / "national_accounts.pkl",
        path_to_growth_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH / country / "growth_accounts.pkl",
    ):
        """Clean the data (Python version)."""
        data_info = read_yaml(depends_on["data_info"])
        capital_accounts, national_accounts = read_data(data_info, country)

        capital_accounts_clean = clean_and_reshape_eu_klems(capital_accounts, data_info)
        national_accounts_clean = clean_and_reshape_eu_klems(
            national_accounts, data_info
        )

        capital_accounts_clean.to_pickle(path_to_capital_accounts)
        national_accounts_clean.to_pickle(path_to_national_accounts)

        if country != "SK":
            growth_accounts = read_growth_accounts(data_info, country)
            growth_accounts_clean = clean_and_reshape_eu_klems(growth_accounts, data_info)
            growth_accounts_clean.to_pickle(path_to_growth_accounts)
        else:
            growth_accounts_clean = pd.DataFrame()
            growth_accounts_clean.to_pickle(path_to_growth_accounts)
