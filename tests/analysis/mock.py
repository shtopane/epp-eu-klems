import pandas as pd

from measuring_intangible_capital.config import INTANGIBLE_DETAIL_CATEGORIES, LABOUR_COMPOSITION_COLUMNS, RNG_FOR_TESTING


def mock_capital_national_accounts() -> tuple[pd.DataFrame, pd.DataFrame]:
  capital_accounts_columns = INTANGIBLE_DETAIL_CATEGORIES + ["tangible_assets"]
  category_dict = {category: RNG_FOR_TESTING.uniform(100, 2000, 5).tolist() for category in capital_accounts_columns}
  capital_accounts = pd.DataFrame(category_dict)
  
  national_accounts = pd.DataFrame({
    "gdp": RNG_FOR_TESTING.uniform(10_000, 100_000, 5).tolist()
  })
  
  return capital_accounts, national_accounts

def mock_growth_accounts() -> pd.DataFrame:
  category_dict = {category: RNG_FOR_TESTING.uniform(0.1, 1.0, 5).tolist() for category in LABOUR_COMPOSITION_COLUMNS}
  growth_accounts = pd.DataFrame(category_dict)
  growth_accounts["labour_productivity"] = RNG_FOR_TESTING.uniform(1.5, 5.0, 5).tolist()

  return growth_accounts
