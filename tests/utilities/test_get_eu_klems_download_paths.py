import re
import pandas as pd
import pytest
from measuring_intangible_capital.config import ALL_COUNTRY_CODES_LESS_SK, COUNTRY_CODES, EU_KLEMS_FILE_NAMES

from measuring_intangible_capital.utilities import get_eu_klems_download_paths

@pytest.mark.parametrize("country_code", [1, None, 1.0, True, False, pd.DataFrame()])
def test_country_code_not_str(country_code):
    with pytest.raises(ValueError, match="country_code"):
        get_eu_klems_download_paths(country_code)

@pytest.mark.parametrize("country_code", ["XX", "XY", "XZ", "banana"])
def test_country_code_not_in_country_codes(country_code):
    with pytest.raises(ValueError, match="is not valid."):
        get_eu_klems_download_paths(country_code)

@pytest.mark.parametrize("country_code", ALL_COUNTRY_CODES_LESS_SK)
def test_return_type_countries_less_SK(country_code):
    result = get_eu_klems_download_paths(country_code)
    
    file_names = list(result.keys())
    assert file_names == EU_KLEMS_FILE_NAMES, "The file names are not correct."

    paths = list(result.values())

    for path in paths:
        assert country_code in str(path), "The country code is not in the path."

def test_return_type_SK():
    country_code = "SK"
    result = get_eu_klems_download_paths(country_code)
    
    file_names = list(result.keys())
    expected_file_names = [file_name for file_name in EU_KLEMS_FILE_NAMES if file_name != "growth_accounts"]
    
    assert file_names == expected_file_names, "The file names are not correct."

    paths = list(result.values())

    for path in paths:
        assert country_code in str(path), "The country code is not in the path."