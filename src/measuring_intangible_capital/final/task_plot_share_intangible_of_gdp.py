from pathlib import Path

import pandas as pd

from measuring_intangible_capital.config import BLD
from measuring_intangible_capital.final.plot import plot_share_intangibles_all_countries


plot_share_intangible_of_gdp_deps = {
    "scripts": [Path("plot.py")],
    "data": BLD / "python" / "share_intangible" / "shares_intangible_of_gdp.pkl",
}

def task_plot_share_intangible_of_gdp(depends_on = plot_share_intangible_of_gdp_deps, plot_save_path = BLD / "figures" / "shares_intangible_investment_gdp.png"):
    """Figure 1: Plot share of intangible investment as percent of GDP for all years and countries.
    Save the plot as png file in the figures folder.
    """
    df = pd.read_pickle(depends_on["data"])
    fig = plot_share_intangibles_all_countries(df)
    fig.write_image(plot_save_path)