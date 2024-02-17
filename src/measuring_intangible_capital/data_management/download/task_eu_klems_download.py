from pathlib import Path
import urllib
from bs4 import BeautifulSoup
from pytask import task
import pytask

from measuring_intangible_capital.data_management.download.eu_klems_download import (
    get_eu_klems_download_page,
    get_urls_file_names_by_country,
)
from measuring_intangible_capital.config import (
    COUNTRY_CODES,
    EU_KLEMS_DATA_DOWNLOAD_PATH,
)

eu_klems_download_deps = {"scripts": Path("eu_klems_download.py")}
eu_klems_download_page: BeautifulSoup = get_eu_klems_download_page()

for country_code in COUNTRY_CODES:
    @pytask.mark.persist 
    @task(id=country_code)
    def task_eu_klems_download(
        page=eu_klems_download_page,
        country_code=country_code,
        depends_on=eu_klems_download_deps,
    ) -> None:
        """Download the EU KLEMS data for selected countries.
        Gather links with country specific data account and download the file.
        """

        urls, file_names = get_urls_file_names_by_country(page, country_code)

        for url, file_name in zip(urls, file_names):
            urllib.request.urlretrieve(
                url, EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / file_name
            )
