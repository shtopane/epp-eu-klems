"""Task for plotting Figure 4a."""
from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.config import BLD, BLD_PYTHON, SRC
from measuring_intangible_capital.plotting.plot import (
    plot_composition_of_labour_productivity,
)

plot_share_intangible_of_gdp_deps = {
    "scripts": [Path("plot.py"), Path(SRC / "analysis" / "intangible_investment.py")],
    "data": BLD_PYTHON / "labour_productivity" / "composition_1995_2006.pkl",
}


def task_plot_labour_composition_average_1995_2006(
    depends_on: dict = plot_share_intangible_of_gdp_deps,
    plot_save_path: Annotated[Path, Product] = BLD / "figures" / "figure_4a.png",
):
    """Figure 4a: Plot share of intangible investment as percent of GDP for all years and countries.
    Save the plot as png file in the figures folder.
    """
    df = pd.read_pickle(depends_on["data"])
    fig = plot_composition_of_labour_productivity(df)
    fig.write_image(plot_save_path)
