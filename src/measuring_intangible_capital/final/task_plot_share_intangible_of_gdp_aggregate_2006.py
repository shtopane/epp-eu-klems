from pathlib import Path

import pandas as pd

from measuring_intangible_capital.config import BLD
from measuring_intangible_capital.final.plot import plot_share_intangible_of_gdp_by_type, plot_share_intangibles_all_countries


plot_share_intangible_of_gdp_aggregate_2006_deps = {
    "scripts": [Path("plot.py")],
    "data": BLD / "python" / "share_intangible" / "shares_intangible_of_gdp_aggregate_2006.pkl",
}

def task_plot_share_intangible_of_gdp_aggregate_2006(depends_on = plot_share_intangible_of_gdp_aggregate_2006_deps, plot_save_path = BLD / "figures" / "shares_intangible_investment_gdp_aggregate_2006.png"):
    """Figure 2: Plot the share of intangible investment of GDP for each country and aggregate category for 2006.
    Each category is: computerized_information, innovative_property, economic_competencies
    Save the plot to the given path.
    """
    df = pd.read_pickle(depends_on["data"])
    fig = plot_share_intangible_of_gdp_by_type(df)
    fig.write_image(plot_save_path)