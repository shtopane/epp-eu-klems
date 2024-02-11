import requests
from pathlib import Path
from bs4 import BeautifulSoup
from measuring_intangible_capital.config import EU_KLEMS_WEBSITE
import urllib

def get_eu_klems_download_page() -> BeautifulSoup:
    """Return a BeautifulSoup object of the EU KLEMS download page."""
    return BeautifulSoup(requests.get(EU_KLEMS_WEBSITE).text, "html.parser")


def get_urls_file_names_by_country(
    page: BeautifulSoup, country_codes: list[str]
) -> tuple[list[str], list[str]]:
    """Return a list of URLs that contain a country code and the extracted file name from the url.
    URLS are download URLS from the EU KLEMS website.
    page: BeautifulSoup object - the EU KLEMS download page
    country_codes: list[str] - a list of country codes to search for in the URLs
    """
    wanted_urls = []
    file_names = []

    for link in page.find_all("a"):
        current_href: str = link.get("href")
        if current_href is not None and not current_href.startswith("#"):
            current_href = current_href
            for code in country_codes:
                if code in current_href:
                    wanted_urls.append(current_href)
                    # example url:
                    # https://www.dropbox.com/s/5usiqokdj2orzlv/SK_intangible%20analytical.xlsx?dl=1
                    # split by SK, then take the second part, and remove the "?dl=1" part
                    file_name = code + current_href.split(code)[1].strip("?dl=1")
                    # replace empty spaces with underscores
                    file_name = file_name.replace("%20", "_")
                    file_names.append(file_name)

    return wanted_urls, file_names

def download_eu_klems(
    file_names: list[str], wanted_urls: list[str], download_folder: Path, country_codes: list[str]
) -> None:
    """Download files from the EU KLEMS website.
    file_names: list[str] - a list of file names to save the files as
    wanted_urls: list[str] - a list of URLs to download
    download_folder: str - the folder to save the files in
    """
    for index, file_name in enumerate(file_names):
        url_of_file = wanted_urls[index]
        for code in country_codes:
          # Create a subfolder for each country code
          if(code in file_name):
            Path(download_folder / code).mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url_of_file, download_folder / Path(code) / file_name)
