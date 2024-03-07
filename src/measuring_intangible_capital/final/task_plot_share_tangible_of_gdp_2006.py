from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.config import BLD, BLD_PYTHON, SRC
from measuring_intangible_capital.final.plot import plot_share_tangible_to_intangible


plot_share_tangible_of_gdp_2006_deps = {
    "scripts": [Path("plot.py"), Path(SRC / "analysis" / "intangible_investment.py")],
    "tangible_investment": BLD_PYTHON / "share_tangible" / "gdp_aggregate_2006.pkl",
    "intangible_investment": BLD_PYTHON / "share_intangible" / "gdp_aggregate_2006.pkl",
}

def task_plot_share_tangible_of_gdp_2006(
        depends_on: dict = plot_share_tangible_of_gdp_2006_deps, 
        plot_save_path: Annotated[Path, Product] = BLD / "figures" / "figure_3.png"
):
    """Figure 3: Plot the share of intangible investment of GDP for each country and aggregate category for 2006.
    Each category is: computerized_information, innovative_property, economic_competencies
    Save the plot to the given path.
    """
    df_intangible = pd.read_pickle(depends_on["intangible_investment"])
    df_tangible = pd.read_pickle(depends_on["tangible_investment"])
    
    fig = plot_share_tangible_to_intangible(
        intangible_df=df_intangible,
        tangible_df=df_tangible
    )
    fig.write_image(plot_save_path)