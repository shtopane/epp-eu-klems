import numpy as np
import pandas as pd
import pytest
from measuring_intangible_capital.analysis.intangible_investment import get_composition_of_value_added, get_intangible_investment_aggregate_types, get_share_of_intangible_investment_per_gdp, get_share_of_tangible_investment_per_gdp
from measuring_intangible_capital.config import ALL_COUNTRY_CODES, INTANGIBLE_AGGREGATE_CATEGORIES, INTANGIBLE_DETAIL_CATEGORIES

from tests.analysis.mock import mock_capital_national_accounts, mock_growth_accounts

@pytest.fixture()
def capital_accounts():
  capital_accounts, _ = mock_capital_national_accounts()
  return capital_accounts

@pytest.fixture()
def national_accounts():
  _, national_accounts = mock_capital_national_accounts()
  return national_accounts

@pytest.fixture()
def capital_accounts_indexed(capital_accounts):
  capital_accounts["country_code"] = ALL_COUNTRY_CODES[0]
  capital_accounts["year"] = 1995
  capital_accounts.set_index(["country_code", "year"], inplace=True)
  return capital_accounts

@pytest.fixture()
def national_accounts_indexed(national_accounts):
  national_accounts["country_code"] = ALL_COUNTRY_CODES[0]
  national_accounts["year"] = 1995

  national_accounts.set_index(["country_code", "year"], inplace=True)
  return national_accounts

@pytest.fixture()
def growth_accounts():
  return mock_growth_accounts()

@pytest.mark.parametrize("capital_accounts", [pd.DataFrame(), pd.DataFrame(columns=["a", "b", "c"])])
def test_get_share_of_intangible_investment_per_gdp_capital_accounts_invalid_columns(capital_accounts, national_accounts):
  with pytest.raises(ValueError, match="capital_accounts has the wrong columns"):
    get_share_of_intangible_investment_per_gdp(
      capital_accounts=capital_accounts,
      national_accounts=national_accounts
    )

@pytest.mark.parametrize("capital_accounts", [1, None, 1.0, True, False, {}])
def test_get_share_of_intangible_investment_per_gdp_capital_accounts_wrong_type(capital_accounts, national_accounts):
  with pytest.raises(ValueError, match="capital_accounts"):
    get_share_of_intangible_investment_per_gdp(
      capital_accounts=capital_accounts,
      national_accounts=national_accounts
    )

@pytest.mark.parametrize("national_accounts", [pd.DataFrame(), pd.DataFrame(columns=["a", "b", "c"])])
def test_get_share_of_intangible_investment_per_gdp_national_accounts_invalid_columns(national_accounts, capital_accounts):
  with pytest.raises(ValueError, match="national_accounts has the wrong columns"):
    get_share_of_intangible_investment_per_gdp(
      capital_accounts=capital_accounts,
      national_accounts=national_accounts
    )

@pytest.mark.parametrize("national_accounts", [1, None, 1.0, True, False, {}])
def test_get_share_of_intangible_investment_per_gdp_national_accounts_wrong_type(national_accounts, capital_accounts):
  with pytest.raises(ValueError, match="national_accounts"):
    get_share_of_intangible_investment_per_gdp(
      capital_accounts=capital_accounts,
      national_accounts=national_accounts
    )

def test_get_share_of_intangible_investment_per_gdp_issue_warning(capital_accounts, national_accounts):
  capital_accounts[INTANGIBLE_DETAIL_CATEGORIES[0]] = 100
  national_accounts["gdp"] = 50
  
  with pytest.warns(UserWarning, match="Share of intangible investment is greater than 100% of GDP"):
    get_share_of_intangible_investment_per_gdp(
      capital_accounts=capital_accounts,
      national_accounts=national_accounts
   )

def test_get_share_of_intangible_investment_per_gdp_investment_level(capital_accounts, national_accounts):
  result = get_share_of_intangible_investment_per_gdp(
    capital_accounts=capital_accounts,
    national_accounts=national_accounts
  )

  expected = capital_accounts[INTANGIBLE_DETAIL_CATEGORIES].sum(axis=1)
  assert result["investment_level"].equals(expected)

def test_get_share_of_intangible_investment_per_gdp_share_intangible_share_intangible_positive(capital_accounts, national_accounts):
  result = get_share_of_intangible_investment_per_gdp(
    capital_accounts=capital_accounts,
    national_accounts=national_accounts
  )

  assert np.all(result["share_intangible"] >= 0)

@pytest.mark.parametrize("growth_accounts", [None, 1, 1.0, True, False, {}])
def test_get_composition_of_value_added_growth_accounts_invalid(growth_accounts):
  with pytest.raises(ValueError, match="growth_accounts"):
    get_composition_of_value_added(
      growth_accounts=growth_accounts,
      country_code=ALL_COUNTRY_CODES[0]
    )

@pytest.mark.parametrize("country_code", [1, None, 1.0, True, False, pd.DataFrame()])
def test_get_composition_of_value_added_country_code_invalid(country_code, growth_accounts):
  with pytest.raises(ValueError, match="country_code"):
    get_composition_of_value_added(
      growth_accounts=growth_accounts,
      country_code=country_code
    )

@pytest.mark.parametrize("growth_accounts", [pd.DataFrame(), pd.DataFrame(columns=["a", "b", "c"])])
def test_get_composition_of_value_added_growth_accounts_wrong_columns(growth_accounts):
  with pytest.raises(ValueError, match="growth_accounts has the wrong columns"):
    get_composition_of_value_added(
      growth_accounts=growth_accounts,
      country_code=ALL_COUNTRY_CODES[0]
    )

def test_get_composition_of_value_added_result_smaller_than_original(growth_accounts):
  actual_first = get_composition_of_value_added(
    growth_accounts=growth_accounts,
    country_code=ALL_COUNTRY_CODES[0]
  )
  actual_first.set_index("country_code", inplace=True)

  growth_accounts_negative_mfp = growth_accounts.copy()
  growth_accounts_negative_mfp["tangible_ICT"] += 10
  
  actual_second = get_composition_of_value_added(
    growth_accounts=growth_accounts_negative_mfp,
    country_code=ALL_COUNTRY_CODES[0]
  )
  actual_second.set_index("country_code", inplace=True)

  growth_accounts_max_value = growth_accounts.max().max()
  actual_first_max_value = actual_first.max().max()
  growth_accounts_negative_mfp_max_value = growth_accounts_negative_mfp.max().max()
  actual_second_max_value = actual_second.max().max()

  assert growth_accounts_max_value > actual_first_max_value
  assert growth_accounts_negative_mfp_max_value > actual_second_max_value
 
def test_get_intangible_investment_aggregate_types_raise_index_not_equal(capital_accounts_indexed, national_accounts):
  national_accounts["country_name"] = "BE"
  national_accounts.set_index("country_name", inplace=True)
  
  with pytest.raises(ValueError, match="Index is not the same"):
    get_intangible_investment_aggregate_types(
      capital_accounts=capital_accounts_indexed,
      national_accounts=national_accounts,
      country_code=ALL_COUNTRY_CODES[0]
    )

def test_get_intangible_investment_aggregate_types_result(capital_accounts_indexed, national_accounts_indexed):
  actual = get_intangible_investment_aggregate_types(
    capital_accounts=capital_accounts_indexed,
    national_accounts=national_accounts_indexed,
    country_code=ALL_COUNTRY_CODES[0]
  )
  assert actual.columns.tolist() == INTANGIBLE_AGGREGATE_CATEGORIES

def test_get_share_of_tangible_investment_per_gdp_index_not_equal(capital_accounts_indexed, national_accounts):
  national_accounts["country_name"] = "BE"
  national_accounts.set_index("country_name", inplace=True)
  
  with pytest.raises(ValueError, match="Index is not the same"):
    get_share_of_tangible_investment_per_gdp(
      capital_accounts=capital_accounts_indexed,
      national_accounts=national_accounts,
      country_code = ALL_COUNTRY_CODES[0]
    )

def test_get_share_of_tangible_investment_per_gdp_result_column(capital_accounts_indexed, national_accounts_indexed):
  actual = get_share_of_tangible_investment_per_gdp(
    capital_accounts=capital_accounts_indexed,
    national_accounts=national_accounts_indexed,
    country_code = ALL_COUNTRY_CODES[0]
  )
  
  assert actual.columns.tolist() == ["share_tangible"]

def test_get_share_of_tangible_investment_per_gdp_result_index_match(capital_accounts_indexed, national_accounts_indexed):
  actual = get_share_of_tangible_investment_per_gdp(
    capital_accounts=capital_accounts_indexed,
    national_accounts=national_accounts_indexed,
    country_code = ALL_COUNTRY_CODES[0]
  )
  
  assert actual.index.equals(capital_accounts_indexed.index)

