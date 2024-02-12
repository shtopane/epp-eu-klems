from pathlib import Path
import urllib
from typing import Annotated
from pytask import task, Product

from measuring_intangible_capital.data_management.download import eu_klems_download
from measuring_intangible_capital.config import COUNTRY_CODES, EU_KLEMS_DATA_DOWNLOAD_PATH

eu_klems_download_deps = {
  "scripts": Path("eu_klems_download.py")
}

for country_code in COUNTRY_CODES:
  @task
  def task_eu_klems_download(
      depends_on = eu_klems_download_deps,
      # partial_path_to_data: Annotated[Path, Product] = EU_KLEMS_DATA_DOWNLOAD_PATH / Path(country)
  ):
      """Download the EU KLEMS data."""
      page = eu_klems_download.get_eu_klems_download_page()
      urls, file_names = eu_klems_download.get_urls_file_names_by_country(page, [country_code])
      
      for index, file_name in enumerate(file_names):
        url_of_file = urls[index]
        
        urllib.request.urlretrieve(url_of_file, EU_KLEMS_DATA_DOWNLOAD_PATH / country_code / file_name)