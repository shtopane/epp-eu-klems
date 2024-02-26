from pathlib import Path
from typing import Annotated
import urllib
from bs4 import BeautifulSoup
from pytask import Product, task
import pytask

from measuring_intangible_capital.data_management.download.eu_klems_download import (
    get_eu_klems_download_page,
    get_urls_file_names_by_country,
)
from measuring_intangible_capital.config import (
    COUNTRY_CODES,
    EU_KLEMS_DATA_DOWNLOAD_PATH,
    EU_KLEMS_FILE_NAMES,
)

eu_klems_download_deps = {"scripts": Path("eu_klems_download.py")}
eu_klems_download_page: BeautifulSoup = get_eu_klems_download_page()


for country in COUNTRY_CODES:
    # Create dynamic paths for each country and types of files(national_accounts, capital_accounts)
    eu_klems_download_products = [
        EU_KLEMS_DATA_DOWNLOAD_PATH / country / f"{filename}.xlsx" for filename in EU_KLEMS_FILE_NAMES
    ]

    @task(id=country)
    def task_eu_klems_download(
        page=eu_klems_download_page,
        country=country,
        depends_on=eu_klems_download_deps,
        path_to_downloaded_data: Annotated[list[Path], Product] = eu_klems_download_products
    ) -> None:
        """Download the EU KLEMS data for selected countries.
        Gather links with country specific data account and download the file.
        """

        urls, file_names = get_urls_file_names_by_country(page, country)
        # assert False
        for url, file_name in zip(urls, file_names):
            urllib.request.urlretrieve(
                url, EU_KLEMS_DATA_DOWNLOAD_PATH / country / file_name
            )
