from pathlib import Path
import os
from typing import Annotated
import urllib
from bs4 import BeautifulSoup
from pytask import Product, task

from measuring_intangible_capital.data_management.download.eu_klems_download import (
    get_eu_klems_download_page,
    get_urls_file_names_by_country,
)
from measuring_intangible_capital.config import COUNTRY_CODES
from measuring_intangible_capital.utilities import get_eu_klems_download_paths

eu_klems_download_deps = {"scripts": Path("eu_klems_download.py")}
eu_klems_download_page: BeautifulSoup = get_eu_klems_download_page()


for country in COUNTRY_CODES:
    eu_klems_download_products = get_eu_klems_download_paths(country)

    @task(id=country)
    def task_eu_klems_download(
        page=eu_klems_download_page,
        country=country,
        depends_on=eu_klems_download_deps,
        path_to_downloaded_data: Annotated[
            dict[str, Path], Product
        ] = eu_klems_download_products,
    ) -> None:
        """Download the EU KLEMS data for selected countries.
        Gather links with country specific data account and download the file.
        """

        urls, file_names = get_urls_file_names_by_country(page, country)

        for url, file_name in zip(urls, file_names):
            file_name_no_extension = os.path.splitext(file_name)[0]
            urllib.request.urlretrieve(
                url, path_to_downloaded_data[file_name_no_extension]
            )
