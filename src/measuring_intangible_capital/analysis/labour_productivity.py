"""Functions for calculating labour productivity."""
import pandas as pd

from measuring_intangible_capital.config import INTANGIBLE_AGGREGATE_CATEGORIES

def get_share_of_intangible_sub_components_in_labour_productivity(df: pd.DataFrame, percentages: list[float]):
    """Calculate the share of intangible sub-components in labour productivity.
    
    Args:
        df (pd.DataFrame): The data frame with the composition of labour productivity growth. For a given country.
        percentages (dict): The percentages of intangible sub-components in labour productivity. For a given country.
    Returns:
        pd.Series: The data frame with the share of intangible sub-components in labour productivity.
    """
    sr = pd.Series()
    intangible_component = df["intangible"]

    intangible_sub_components = [round(intangible_component * percentage, 3) for percentage in percentages]

    for index, column in enumerate(INTANGIBLE_AGGREGATE_CATEGORIES):
        sr[column] = intangible_sub_components[index]
        sr.name = column
    
    return sr
