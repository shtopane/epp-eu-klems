"""Functions to download data from the EU KLEMS website."""

import requests
from bs4 import BeautifulSoup
import re

from measuring_intangible_capital.config import EU_KLEMS_WEBSITE, FILES_TO_EXCLUDE

def _links_not_excluded(href) -> bool:
    """Search only for links that do not contain the files to exclude.
    In our case, we don't use the growth accounts data, so we exclude it from the download.
    Args:
        href : the link on the page. Passed by BeautifulSoup.find_all

    Returns:
        bool : whether the given href is allowed or not.
    """
    return href and not re.compile('|'.join(FILES_TO_EXCLUDE)).search(href)

def get_eu_klems_download_page() -> BeautifulSoup:
    """Return a BeautifulSoup object of the EU KLEMS download page.
    Access HTML tags, attributes and content from the EU KLEMS download page.
    Example: page.title # <title>EU KLEMS</title>
    """
    return BeautifulSoup(requests.get(EU_KLEMS_WEBSITE).text, "html.parser")

def get_urls_file_names_by_country(
    page: BeautifulSoup, country_code: str
) -> tuple[list[str], list[str]]:
    """Return a list of URLs that contain a country code and the
    extracted file name from the url.

    Args:
        page (BeautifulSoup): the EU KLEMS download page
        country_codes: (str): a country code to filter the download links
    Returns:
        tuple[list[str], list[str]]: tuple of lists containing the URLs and file names for the
        selected country. Download links are for at most 5 files per country.
        Growth accounts, intangible analytics data, labour and capital accounts and national accounts.
    """
    country_urls = []
    file_names = []

    for link in page.find_all(href=_links_not_excluded):
        current_href: str = link.get("href")
        if current_href is not None and not current_href.startswith("#"):
            current_href = current_href
            if country_code in current_href:
                country_urls.append(current_href)
                # example url:
                # https://www.dropbox.com/s/5usiqokdj2orzlv/SK_intangible%20analytical.xlsx?dl=1
                # end result should be "intangible_analytical.xlsx"
                file_name = current_href.split(country_code)[1].strip(
                    "?dl=1"
                )[1:]
                file_name = file_name.replace("%20", "_")

                file_names.append(file_name)

    return country_urls, file_names
