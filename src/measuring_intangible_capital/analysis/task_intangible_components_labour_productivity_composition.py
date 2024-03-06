from pathlib import Path
import pandas as pd

from measuring_intangible_capital.analysis.labour_productivity import (
    get_share_of_intangible_sub_components_in_labour_productivity,
)

from measuring_intangible_capital.config import (
    BLD_PYTHON,
    COUNTRY_CODES_LESS_SK,
    INTANGIBLE_AGGREGATE_CATEGORIES,
)
from measuring_intangible_capital.utilities import (
    get_percent_of_intangible_sub_components_in_labour_productivity,
)


intangible_components_labour_productivity_composition_deps = {
    "scripts": [Path("labour_productivity.py")],
    "data": Path(BLD_PYTHON / "labour_productivity" / "composition.pkl"),
}


def task_intangible_components_labour_productivity_composition(
    depends_on=intangible_components_labour_productivity_composition_deps,
    path_to_data: Path = BLD_PYTHON / "labour_productivity" / "intangible_composition.pkl",
):
    labour_productivity_composition = pd.read_pickle(depends_on["data"])

    df = pd.DataFrame(
        index=labour_productivity_composition.index,
        columns=INTANGIBLE_AGGREGATE_CATEGORIES,
    )

    for country_code in COUNTRY_CODES_LESS_SK:
        labour_composition_for_country = labour_productivity_composition.loc[
            country_code
        ]
        intangible_composition = labour_composition_for_country["intangible"]

        percentages = get_percent_of_intangible_sub_components_in_labour_productivity()
        percentages_for_country = percentages[country_code]

        sub_components = get_share_of_intangible_sub_components_in_labour_productivity(
            intangible_composition, percentages_for_country
        )

        df.loc[country_code, :] = sub_components

    pd.to_pickle(df, path_to_data)
