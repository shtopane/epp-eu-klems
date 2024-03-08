
from pathlib import Path
from typing import Annotated

from pytask import Product

from measuring_intangible_capital.config import DATA_CLEAN_PATH, SRC
from measuring_intangible_capital.data_management.clean_gdp_data import clean_gdp_per_capita, read_data
from measuring_intangible_capital.utilities import read_yaml


clean_gdp_per_capita_deps = {
    "scripts": Path("clean_gdp_data.py"),
    "data": SRC / "data_management" / "data" / "GDP_per_capita_PPP.xlsx",
    "data_info": SRC / "data_management" / "gdp_data_info.yaml",

}
def task_clean_gdp_per_capita(
        depends_on: dict = clean_gdp_per_capita_deps,
        path_to_gdp_per_capita: Annotated[Path, Product] = Path(DATA_CLEAN_PATH / "gdp" / "gdp_per_capita.pkl"),
):
    """Clean the GDP per capita data from the World Bank."""
    data_info = read_yaml(depends_on["data_info"])
    raw = read_data(depends_on["data"], data_info)
    data_clean = clean_gdp_per_capita(raw, data_info)

    data_clean.to_pickle(path_to_gdp_per_capita)