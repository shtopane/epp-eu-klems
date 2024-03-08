from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product

from measuring_intangible_capital.config import BLD, BLD_PYTHON
from measuring_intangible_capital.plotting.plot import (
    plot_sub_components_intangible_labour_productivity,
)


plot_intangible_components_labour_composition_deps = {
    "scripts": [Path("plot.py")],
    "data": Path(BLD_PYTHON / "labour_productivity" / "intangible_composition.pkl"),
}


def task_plot_intangible_components_labour_composition(
    depends_on=plot_intangible_components_labour_composition_deps,
    plot_save_path: Annotated[Path, Product] = Path(BLD / "figures" / "figure_4b.png"),
):
    """Figure 4b: Plot the share of intangible investment as percent of GDP for all years and countries."""
    df = pd.read_pickle(depends_on["data"])
    
    fig = plot_sub_components_intangible_labour_productivity(df)
    fig.write_image(plot_save_path)
