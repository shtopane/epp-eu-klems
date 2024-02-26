from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.config import BLD, BLD_PYTHON, SRC
from measuring_intangible_capital.final.plot import plot_share_intangibles_all_countries


plot_share_intangible_of_gdp_deps = {
    "scripts": [Path("plot.py"), Path(SRC / "analysis" / "intangible_investment.py")],
    "data": BLD_PYTHON / "share_intangible" / "gdp_aggregate_1995_2006.pkl",
}

def task_plot_share_intangible_of_gdp(
        depends_on: dict = plot_share_intangible_of_gdp_deps, 
        plot_save_path: Annotated[Path, Product] = BLD / "figures" / "figure_1b.png"):
    """Figure 1: Plot share of intangible investment as percent of GDP for all years and countries.
    Save the plot as png file in the figures folder.
    """
    df = pd.read_pickle(depends_on["data"])
    fig = plot_share_intangibles_all_countries(df)
    fig.write_image(plot_save_path)