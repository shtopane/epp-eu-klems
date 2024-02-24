from pathlib import Path

import pandas as pd

from measuring_intangible_capital.config import BLD
from measuring_intangible_capital.final.plot import plot_share_intangible_of_gdp_by_type, plot_share_intangibles_all_countries, plot_share_tangible_to_intangible


plot_share_tangible_of_gdp_2006_deps = {
    "scripts": [Path("plot.py")],
    "tangible_investment": BLD / "python" / "share_intangible" / "shares_tangible_of_gdp_2006.pkl",
    "intangible_investment": BLD / "python" / "share_intangible" / "shares_intangible_of_gdp_aggregate_2006.pkl",
}

def task_plot_share_tangible_of_gdp_2006(depends_on = plot_share_tangible_of_gdp_2006_deps, plot_save_path = BLD / "figures" / "shares_tangible_intangible_gdp_2006.png"):
    """Figure 3: Plot the share of intangible investment of GDP for each country and aggregate category for 2006.
    Each category is: computerized_information, innovative_property, economic_competencies
    Save the plot to the given path.
    """
    df_tangible = pd.read_pickle(depends_on["tangible_investment"])
    df_tangible = df_tangible.set_index("country_code")
    df_intangible = pd.read_pickle(depends_on["intangible_investment"])

    df_intangible_sum = pd.DataFrame()
    df_intangible_sum["intangible_assets"] = df_intangible.set_index("country_code").sum(axis=1)

    df = pd.concat([df_tangible, df_intangible_sum], axis=1).reset_index()

    fig = plot_share_tangible_to_intangible(df)

    fig.write_image(plot_save_path)