import re
import numpy as np
import pandas as pd
import pytest
from measuring_intangible_capital.config import COUNTRIES, COUNTRY_CODES

from measuring_intangible_capital.utilities import _add_country_name

@pytest.fixture
def empty_valid_df():
   return pd.DataFrame(columns=["country_code"])

@pytest.fixture
def austria_df():
   return pd.DataFrame({"country_code": ["AT"]})

@pytest.fixture
def all_countries_df():
    return pd.DataFrame({"country_code": COUNTRY_CODES})

def test_input_not_data_frame_error():
    with pytest.raises(ValueError, match=re.escape("The input is not a pandas DataFrame.")):
      _add_country_name(None)

def test_missing_country_code_error():
    with pytest.raises(ValueError, match=re.escape("The data frame does not contain a column 'country_code'.")):
      _add_country_name(pd.DataFrame())

def test_empty_column(empty_valid_df):
   result = _add_country_name(empty_valid_df)
   assert result.equals(empty_valid_df)

def test_return_value(austria_df):
   result = _add_country_name(austria_df)
   assert result[0] == "Austria"

def test_all_countries(all_countries_df):
    result = _add_country_name(all_countries_df)
    assert len(result) == len(COUNTRY_CODES), "The result is and countries array don't match."
    assert np.array_equal(result.values, COUNTRIES), "The result is and countries array don't match."