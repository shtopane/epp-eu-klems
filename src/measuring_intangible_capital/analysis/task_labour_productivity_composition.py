from pathlib import Path
from typing import Annotated
import pandas as pd

from pytask import Product
from measuring_intangible_capital.analysis.intangible_investment import get_composition_of_value_added

from measuring_intangible_capital.config import BLD_PYTHON, COUNTRY_CODES, COUNTRY_CODES_LESS_SK, DATA_CLEAN_PATH


labour_productivity_composition_deps = {
  "scripts": [Path("intangible_investment.py")],
  "growth_accounts": [Path(DATA_CLEAN_PATH / country_code / "growth_accounts.pkl") for country_code in COUNTRY_CODES_LESS_SK],
}
def task_labour_productivity_composition(
    depends_on=labour_productivity_composition_deps,
    path_to_labour_productivity_composition: Annotated[Path, Product] = BLD_PYTHON / "labour_productivity" / "composition.pkl"
):
    """Calculate the composition of labour productivity growth for each country.
    For each country, select the growth accounts data for the years 1995 to 2006 and calculate the composition of labour productivity growth.
    Store the data frame for each country and concatenate at the end.
    The result is a data frame for all countries with columns: year, country, composition.
    Lastly, save the data frame to a pickle file.
    """
    years = range(1995, 2007)
    dfs = []

    for index, country_code in enumerate(COUNTRY_CODES_LESS_SK):
        growth_accounts: pd.DataFrame = pd.read_pickle(depends_on["growth_accounts"][index])
        growth_accounts_for_years = growth_accounts.loc[:, list(years), :]
        
        df = get_composition_of_value_added(growth_accounts_for_years, country_code)
        dfs.append(df)
    
    labour_productivity_growth_composition = pd.concat(dfs)
    labour_productivity_growth_composition = labour_productivity_growth_composition.set_index("country_code")
    
    pd.to_pickle(labour_productivity_growth_composition, path_to_labour_productivity_composition)