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
  """Calculate share of intangible investment of GDP for a country."""
  years = range(1995, 2007)
  dfs_merged = []

  for country_code in COUNTRY_CODES:
    capital_accounts_for_years, national_accounts_for_years = get_country_total_gdp_investment(country_code, years)
    data_merged = get_share_of_intangible_investment_per_gdp(capital_accounts_for_years, national_accounts_for_years)
    dfs_merged.append(data_merged)
  
  data_for_plotting = pd.concat(dfs_merged)

  pd.to_pickle(data_for_plotting, path_to_shares_intangible)