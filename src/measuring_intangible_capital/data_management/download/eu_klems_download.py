"""Functions to download data from the EU KLEMS website."""

import requests
from bs4 import BeautifulSoup
import re

from measuring_intangible_capital.config import EU_KLEMS_WEBSITE, FILES_TO_EXCLUDE

def _links_not_excluded(href) -> bool:
    """Filter the links that are not allowed.
    In our case, we don't use the growth accounts data, so we exclude it from the download.
    Args:
        href : the link on the page. Passed by BeautifulSoup.find_all

    Returns:
        bool : whether the given href is allowed or not.
    """
    return href and not re.compile('|'.join(FILES_TO_EXCLUDE)).search(href)

def _clear_file_name(href: str, country_code: str) -> str:
    """Extract the file name from the URL and clean it.
    Example:
        https://www.dropbox.com/s/5usiqokdj2orzlv/SK_intangible%20analytical.xlsx?dl=1 -> intangible_analytical.xlsx
    Args:
        href (str): the URL of the file
        country_code (str): country_code contained in the URL

    Returns:
        str: the cleaned file name
    """
    file_name = href.split(country_code)[1].strip(
        "?dl=1"
    )[1:]
    file_name = file_name.replace("%20", "_")

    return file_name

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
    In the EU KLEMS website, there are download links for every country data set.
    This function deals with the extraction of the file names and urls of the download links.

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
            if country_code in current_href:
                country_urls.append(current_href)
                file_name = _clear_file_name(current_href, country_code)
                file_names.append(file_name)

    return country_urls, file_names
