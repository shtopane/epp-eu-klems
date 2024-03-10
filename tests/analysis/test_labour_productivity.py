import pandas as pd
import pytest
from measuring_intangible_capital.analysis.labour_productivity import get_share_of_intangible_sub_components_in_labour_productivity
from measuring_intangible_capital.config import INTANGIBLE_AGGREGATE_CATEGORIES

@pytest.fixture
def percentages():
  return [0.5, 0.3, 0.2]

@pytest.mark.parametrize("percentages", ["1", 1, 1.0, True, False, pd.DataFrame()])
def test_get_share_of_intangible_sub_components_in_labour_productivity_invalid(percentages):
  with pytest.raises(ValueError, match="<class 'list'>"):
    get_share_of_intangible_sub_components_in_labour_productivity(
      percentages=percentages
    )

def test_get_share_of_intangible_sub_components_in_labour_productivity_length_mismatch(percentages):
  percentages = percentages[1:]
  
  with pytest.raises(ValueError, match=f"2"):
    get_share_of_intangible_sub_components_in_labour_productivity(
      percentages=percentages
    )

def test_get_share_of_intangible_sub_components_in_labour_productivity_result_columns(percentages):
  actual = get_share_of_intangible_sub_components_in_labour_productivity(
    percentages=percentages
  )

  assert actual.index.tolist() == INTANGIBLE_AGGREGATE_CATEGORIES

def test_get_share_of_intangible_sub_components_in_labour_productivity_result_values(percentages):
  actual = get_share_of_intangible_sub_components_in_labour_productivity(
    percentages=percentages
  )

  assert actual.values.tolist() == percentages