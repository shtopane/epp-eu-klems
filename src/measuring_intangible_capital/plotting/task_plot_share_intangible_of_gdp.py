from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.config import (
    BLD,
    BLD_PYTHON,
    SRC,
)
from measuring_intangible_capital.plotting.plot import (
    plot_share_intangibles_for_extended_countries,
    plot_share_intangibles_for_main_countries,
)


plot_share_intangible_of_gdp_deps = {
    "scripts": [Path("plot.py"), Path(SRC / "analysis" / "intangible_investment.py")],
    "data": BLD_PYTHON / "share_intangible" / "gdp_aggregate_1995_2006.pkl",
}


def task_plot_share_intangible_of_gdp(
    depends_on: dict = plot_share_intangible_of_gdp_deps,
    plot_save_path_figure1b: Annotated[Path, Product] = BLD / "figures" / "figure_1b.png",
    plot_save_path_figure1a: Annotated[Path, Product] = BLD / "figures" / "figure_1a.png",
):
    """Figure 1: Plot share of intangible investment as percent of GDP for 2006 for selected countries.
    This task produces two figures: Figure 1a and Figure 1b.
    Figure 1a: Share of intangible investment as percent of GDP for 2006 for US, UK, DE, FR, ES, and IT.
    Figure 1b: Share of intangible investment as percent of GDP for 2006 for AT, CZ, DK, EL, SK.
    
    Save the plot as png file in the figures folder.
    """
    df = pd.read_pickle(depends_on["data"])

    fig_main_countries = plot_share_intangibles_for_main_countries(df)
    fig_extended_countries = plot_share_intangibles_for_extended_countries(df)

    fig_main_countries.write_image(plot_save_path_figure1b)
    fig_extended_countries.write_image(plot_save_path_figure1a)
