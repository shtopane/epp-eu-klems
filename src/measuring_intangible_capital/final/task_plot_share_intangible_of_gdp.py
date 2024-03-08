from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.config import (
    BLD,
    BLD_PYTHON,
    COUNTRY_CODES,
    COUNTRY_CODES_EXTENDED,
    COUNTRY_COLOR_MAP,
    COUNTRY_COLOR_MAP_EXTENDED,
    SRC,
)
from measuring_intangible_capital.final.plot import plot_share_intangibles_for_countries


plot_share_intangible_of_gdp_deps = {
    "scripts": [Path("plot.py"), Path(SRC / "analysis" / "intangible_investment.py")],
    "data": BLD_PYTHON / "share_intangible" / "gdp_aggregate_1995_2006.pkl",
}


def task_plot_share_intangible_of_gdp(
    depends_on: dict = plot_share_intangible_of_gdp_deps,
    plot_save_path_figure1b: Annotated[Path, Product] = BLD
    / "figures"
    / "figure_1b.png",
    plot_save_path_figure1a: Annotated[Path, Product] = BLD
    / "figures"
    / "figure_1a.png",
):
    """Figure 1: Plot share of intangible investment as percent of GDP for
    Austria, Czech Republic, Denmark, Greece, and Slovakia(1995-2006).
    Figure 1a: Plot share of intangible investment as percent of GDP for France, Germany, Italy, Spain, the UK and the US
    Save the plot as png file in the figures folder.
    """
    df = pd.read_pickle(depends_on["data"])

    fig_main_countries = plot_share_intangibles_for_countries(
        df,
        country_codes=COUNTRY_CODES,
        country_color_map=COUNTRY_COLOR_MAP,
        mode="main",
    )

    fig_extended_countries = plot_share_intangibles_for_countries(
        df,
        country_codes=COUNTRY_CODES_EXTENDED,
        country_color_map=COUNTRY_COLOR_MAP_EXTENDED,
        mode="extended",
    )

    fig_main_countries.write_image(plot_save_path_figure1b)
    fig_extended_countries.write_image(plot_save_path_figure1a)
