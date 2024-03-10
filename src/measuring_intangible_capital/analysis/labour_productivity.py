"""Functions for calculating labour productivity."""

import pandas as pd

from measuring_intangible_capital.config import INTANGIBLE_AGGREGATE_CATEGORIES
from measuring_intangible_capital.error_handling_utilities import raise_variable_none, raise_variable_wrong_type


def get_share_of_intangible_sub_components_in_labour_productivity(percentages: list[float]):
    """Calculate the share of intangible sub-components in labour productivity.

    Args:
        percentages (list[float]): The percentages of intangible sub-components in labour productivity. For a given country.
    Returns:
        pd.Series: The data frame with the share of intangible sub-components in labour productivity.
    """
    raise_variable_none(percentages, "percentages")
    raise_variable_wrong_type(percentages, list, "percentages")
    _raise_length_mismatch(percentages)
    
    sr = pd.Series(index = INTANGIBLE_AGGREGATE_CATEGORIES)

    for index, column in enumerate(INTANGIBLE_AGGREGATE_CATEGORIES):
        sr[column] = percentages[index]

    return sr

def _raise_length_mismatch(percentages):
    if len(percentages) != len(INTANGIBLE_AGGREGATE_CATEGORIES):
        raise ValueError(
            f"The length of the percentages list is {len(percentages)}, but it should be {len(INTANGIBLE_AGGREGATE_CATEGORIES)}"
        )


def get_percent_of_intangible_sub_components_in_labour_productivity():
    """These are real values from the paper.(Table 4)
    Slovakia is missing, since it is not included in the paper figures either.
    Use the percentages to calculate the share of intangible sub-components in labour productivity
    from total intangible capital deepening.
    Round to 2 decimal points.
    Returns:
        dict[list]: the share of each sub-category of intangible capital(software, R&D, etc) in labour productivity.
        Example:
        {
            "AT": [0.13, 0.29, 0.13], soft_db, innovative_property, economic_competencies
        }
    """

    intangible_capital_deepening_by_sub_component_all_countries_less_sk = {
        "AT": [0.13, 0.29, 0.13],
        "DK": [0.29, 0.27, 0.17],
        "CZ": [0.06, 0.35, 0.27],
        "EL": [0.06, 0.11, 0.07],
        "UK": [0.16, 0.17, 0.36],
        "US": [0.18, 0.35, 0.29],
        "DE": [0.07, 0.23, 0.07],
        "FR": [0.15, 0.18, 0.15],
        "IT": [0.03, 0.05, 0.04],
        "ES": [0.05, 0.15, -0.08],
    }

    return intangible_capital_deepening_by_sub_component_all_countries_less_sk
