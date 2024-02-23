# """Tasks running the core analyses."""

from pathlib import Path
import pandas as pd

from pytask import task

from measuring_intangible_capital.config import BLD, COUNTRY_CODES
from measuring_intangible_capital.analysis.intangible_investment import get_country_total_gdp_investment, get_share_of_intangible_investment_per_gdp

share_intangible_of_gdp_deps = {
    "scripts": [Path("intangible_investment.py")]
}

def task_share_intangible_of_gdp(
  depends_on=share_intangible_of_gdp_deps,
  path_to_shares_intangible = BLD / "python" / "share_intangible" / "shares_intangible_of_gdp.pkl"
):
  """Calculate share of intangible investment of GDP for a country from 1995 until 2006.
  For each country, select the capital and national accounts data 
  for the years 1995 to 2006 and get the total values for the whole economy(all industries).
  Then calculate the share of intangible investment of GDP for each year and country.
  Store the data frame for each country and concatenate at the end.
  The result is a data frame for all countries with columns: year, country, share_intangible, intangible_gdp.
  Lastly, save the data frame to a pickle file.
  """
  years = range(1995, 2007)
  dfs = []

  for country_code in COUNTRY_CODES:
    capital_accounts_for_years, national_accounts_for_years = get_country_total_gdp_investment(country_code, years)
    df = get_share_of_intangible_investment_per_gdp(capital_accounts_for_years, national_accounts_for_years)
    dfs.append(df)
  
  data_for_plotting = pd.concat(dfs)

  pd.to_pickle(data_for_plotting, path_to_shares_intangible)