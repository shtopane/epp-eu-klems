"""Task to store components of intangible investments in labour productivity."""
from pathlib import Path
from typing import Annotated

import pandas as pd
from pytask import Product

from measuring_intangible_capital.analysis.labour_productivity import (
    get_percent_of_intangible_sub_components_in_labour_productivity,
    get_share_of_intangible_sub_components_in_labour_productivity,
)
from measuring_intangible_capital.config import (
    ALL_COUNTRY_CODES_LESS_SK,
    BLD_PYTHON,
    INTANGIBLE_AGGREGATE_CATEGORIES,
)

intangible_components_labour_productivity_composition_deps = {
    "scripts": [Path("labour_productivity.py")],
    "data": Path(BLD_PYTHON / "labour_productivity" / "composition_1995_2006.pkl"),
}


def task_intangible_components_labour_productivity_composition(
    depends_on=intangible_components_labour_productivity_composition_deps,
    path_to_data: Annotated[Path, Product] = BLD_PYTHON
    / "labour_productivity"
    / "intangible_composition.pkl",
):
    """Store share of each intangible investment aggregate category in labour
    productivity."""
    labour_productivity_composition = pd.read_pickle(depends_on["data"])

    df = pd.DataFrame(
        index=labour_productivity_composition.index,
        columns=INTANGIBLE_AGGREGATE_CATEGORIES,
    )

    for country_code in ALL_COUNTRY_CODES_LESS_SK:
        percentages = get_percent_of_intangible_sub_components_in_labour_productivity()
        percentages_for_country = percentages[country_code]
        sub_components = get_share_of_intangible_sub_components_in_labour_productivity(
            percentages_for_country,
        )
        df.loc[country_code, :] = sub_components

    pd.to_pickle(df, path_to_data)
