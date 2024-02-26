"""Tasks for managing the data."""

from pathlib import Path
from typing import Annotated

from pytask import Product, task

from measuring_intangible_capital.config import BLD, COUNTRY_CODES, DATA_CLEAN_PATH, EU_KLEMS_DATA_DOWNLOAD_PATH, EU_KLEMS_FILE_NAMES, SRC
from measuring_intangible_capital.utilities import read_yaml
from measuring_intangible_capital.data_management.clean_data import (
    read_data,
    clean_and_reshape_eu_klems,
)

clean_data_deps = {
    "scripts": Path("clean_data.py"),
    "data_info": SRC / "data_management" / "data_info.yaml"
}

for country in COUNTRY_CODES:

    clean_data_deps[f"data_{country}"] = [
        EU_KLEMS_DATA_DOWNLOAD_PATH / country / f"{filename}.xlsx" for filename in EU_KLEMS_FILE_NAMES
    ]
    
    @task(id=country)
    def task_clean_and_reshape_eu_klems(
        country: str = country,
        depends_on = clean_data_deps,
        path_to_capital_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH / country / "capital_accounts.pkl",
        path_to_national_accounts: Annotated[Path, Product] = DATA_CLEAN_PATH / country / "national_accounts.pkl",
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
