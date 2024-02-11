from pathlib import Path
from measuring_intangible_capital.data_management.download import eu_klems_download
from measuring_intangible_capital.config import COUNTRY_CODES, DATA
eu_klems_download_deps = {
  "scripts": Path("eu_klems_download.py")
}

for country in COUNTRY_CODES:

  def task_eu_klems_download(
      depends_on=eu_klems_download_deps,
      produces=DATA / Path(country) / "data.xsls",
  ):
      """Download the EU KLEMS data."""
      eu_klems_download(country, produces)