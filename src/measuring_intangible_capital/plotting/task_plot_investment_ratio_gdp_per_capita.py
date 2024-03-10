"""Task for plotting Figure 5b."""


from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.config import BLD, BLD_PYTHON, DATA_CLEAN_PATH, SRC
from measuring_intangible_capital.plotting.plot import (
    plot_investment_ratio_gdp_per_capita,
)

plot_investment_ratio_gdp_per_capita_deps = {
    "scripts": [Path("plot.py"), Path(SRC / "analysis" / "intangible_investment.py")],
    "intangible_investment": BLD_PYTHON
    / "share_intangible"
    / "gdp_aggregate_2000_2004.pkl",
    "tangible_investment": BLD_PYTHON
    / "share_tangible"
    / "gdp_aggregate_2000_2004.pkl",
    "gdp_per_capita": DATA_CLEAN_PATH / "gdp" / "gdp_per_capita.pkl",
}


def task_plot_investment_ratio_gdp_per_capita(
    depends_on: dict = plot_investment_ratio_gdp_per_capita_deps,
    plot_save_path: Annotated[Path, Product] = BLD / "figures" / "figure_5b.png",
):
    """Figure 5b: Plot the ratio between intangible and tangible investment and GDP per
    capita for all years and countries."""
    gdp_per_capita = pd.read_pickle(depends_on["gdp_per_capita"])
    intangible_investment = pd.read_pickle(depends_on["intangible_investment"])
    tangible_investment = pd.read_pickle(depends_on["tangible_investment"])

    fig = plot_investment_ratio_gdp_per_capita(
        intangible_investment=intangible_investment,
        tangible_investment=tangible_investment,
        gdp_per_capita=gdp_per_capita,
    )
    fig.write_image(plot_save_path)
