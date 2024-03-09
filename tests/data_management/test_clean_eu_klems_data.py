import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from measuring_intangible_capital.config import TEST_DIR
from measuring_intangible_capital.data_management import clean_eu_klems_data
from measuring_intangible_capital.utilities import read_yaml
from tests.data_management.mock import EU_KLEMS_FIXTURE_PATH, MOCK_YEARS_RANGE, mock_eu_klems_data, save_mock_eu_klems_data



@pytest.fixture(scope="module", autouse=True)
def create_mock_data(request):
    print("Creating mock data")
    capital_accounts, national_accounts, growth_accounts = mock_eu_klems_data()
    save_mock_eu_klems_data(capital_accounts, national_accounts, growth_accounts)

    def remove_mock_data():
        print("Removing mock data")
        os.remove(EU_KLEMS_FIXTURE_PATH)

    request.addfinalizer(remove_mock_data)

@pytest.fixture()
def years_range():
    return MOCK_YEARS_RANGE

@pytest.fixture()
def capital_accounts(data_info):
    capital_accounts, _ = clean_eu_klems_data.read_data(
        data_info=data_info,
        path_to_capital_accounts=EU_KLEMS_FIXTURE_PATH,
        path_to_national_accounts=EU_KLEMS_FIXTURE_PATH
    )

    return capital_accounts

@pytest.fixture()
def national_accounts(data_info):
    _, national_accounts = clean_eu_klems_data.read_data(
        data_info=data_info,
        path_to_capital_accounts=EU_KLEMS_FIXTURE_PATH,
        path_to_national_accounts=EU_KLEMS_FIXTURE_PATH
    )

    return national_accounts

@pytest.fixture()
def growth_accounts(data_info):
    growth_accounts = clean_eu_klems_data.read_growth_accounts(
        data_info=data_info,
        path_to_growth_accounts=EU_KLEMS_FIXTURE_PATH
    )

    return growth_accounts


@pytest.fixture()
def data_info():
    return read_yaml(TEST_DIR / "data_management" / "eu_klems_data_info_fixture.yaml")

def test_read_data_return_type(data_info):
    accounts1, accounts2 = clean_eu_klems_data.read_data(
        data_info=data_info, 
        path_to_capital_accounts=EU_KLEMS_FIXTURE_PATH, 
        path_to_national_accounts=EU_KLEMS_FIXTURE_PATH
    )

    assert type(accounts1) == list
    assert type(accounts2) == list

    assert type(accounts1[0]) == pd.DataFrame
    assert type(accounts2[0]) == pd.DataFrame

@pytest.mark.parametrize("data_info", [None, 1, 1.0, True, False, "banana"])
def test_read_data_data_info_not_dict(data_info):
    with pytest.raises(TypeError, match="The data_info argument must be a dictionary."):
        clean_eu_klems_data.read_data(
            data_info=data_info, 
            path_to_capital_accounts=EU_KLEMS_FIXTURE_PATH, 
            path_to_national_accounts=EU_KLEMS_FIXTURE_PATH
        )

@pytest.mark.parametrize("data_info", [{}, {"sheets_to_read": {}}, {"key1": {"key2": {}}}])
def test_read_data_data_info_missing_keys(data_info):
    with pytest.raises(KeyError, match="The data_info dictionary must contain"):
        clean_eu_klems_data.read_data(
            data_info=data_info, 
            path_to_capital_accounts=EU_KLEMS_FIXTURE_PATH, 
            path_to_national_accounts=EU_KLEMS_FIXTURE_PATH
        )

def test_read_data_capital_path_not_valid(data_info):
    with pytest.raises(TypeError, match="Argument path_to_capital_accounts must be a pathlib.Path object."):
        clean_eu_klems_data.read_data(
            data_info=data_info, 
            path_to_capital_accounts="banana", 
            path_to_national_accounts=EU_KLEMS_FIXTURE_PATH
        )

def test_read_data_national_path_not_valid(data_info):
    with pytest.raises(TypeError, match="Argument path_to_national_accounts must be a pathlib.Path object."):
        clean_eu_klems_data.read_data(
            data_info=data_info, 
            path_to_capital_accounts=EU_KLEMS_FIXTURE_PATH,
            path_to_national_accounts="banana"
        )

def test_read_growth_accounts_return_type(data_info):
    growth_accounts = clean_eu_klems_data.read_growth_accounts(
        data_info=data_info, 
        path_to_growth_accounts=EU_KLEMS_FIXTURE_PATH
    )
    assert type(growth_accounts) == list
    assert type(growth_accounts[0]) == pd.DataFrame

@pytest.mark.parametrize("data_info", [None, 1, 1.0, True, False, "banana"])
def test_read_growth_accounts_data_info_not_dict(data_info):
    with pytest.raises(TypeError, match="The data_info argument must be a dictionary."):
        clean_eu_klems_data.read_growth_accounts(
            data_info=data_info, 
            path_to_growth_accounts=EU_KLEMS_FIXTURE_PATH
        )

@pytest.mark.parametrize("data_info", [{}, {"sheets_to_read": {}}, {"key1": {"key2": {}}}])
def test_read_growth_accounts_data_info_missing_keys(data_info):
    with pytest.raises(KeyError, match="The data_info dictionary must contain"):
        clean_eu_klems_data.read_growth_accounts(
            data_info=data_info, 
            path_to_growth_accounts=EU_KLEMS_FIXTURE_PATH
        )

def test_read_growth_accounts_capital_path_not_valid(data_info):
    with pytest.raises(TypeError, match="Argument path_to_growth_accounts must be a pathlib.Path object."):
        clean_eu_klems_data.read_growth_accounts(
            data_info=data_info, 
            path_to_growth_accounts="banana"
        )

@pytest.mark.parametrize("raw", [None, 1, 1.0, True, False, "banana", []])
def test_clean_and_reshape_eu_klems_invalid_data(raw, data_info):
    with pytest.raises(BaseException):
        clean_eu_klems_data.clean_and_reshape_eu_klems(
            raw=raw, 
            data_info=data_info,
        )

def test_clean_and_reshape_eu_klems_return_type(capital_accounts, data_info, years_range):
    capital_accounts_clean = clean_eu_klems_data.clean_and_reshape_eu_klems(
        raw=capital_accounts,
        data_info=data_info,
        years=years_range
    )
    assert type(capital_accounts_clean) == pd.DataFrame

def test_clean_and_reshape_eu_klems_dropna(capital_accounts, data_info, years_range):
    capital_accounts_clean = clean_eu_klems_data.clean_and_reshape_eu_klems(
        raw=capital_accounts,
        data_info=data_info,
        years=years_range
    )
    assert not capital_accounts_clean.isna().any(axis=None)

def test_clean_and_reshape_eu_klems_categorical_columns(capital_accounts, data_info, years_range):
    capital_accounts_clean = clean_eu_klems_data.clean_and_reshape_eu_klems(
        raw=capital_accounts,
        data_info=data_info,
        years=years_range
    )

    capital_accounts_clean = capital_accounts_clean.reset_index()
    
    for cat_col in data_info["categorical_columns"]:
        renamed_col = data_info["column_rename_mapping"].get(cat_col, cat_col)
        assert capital_accounts_clean[renamed_col].dtype == "category"

def test_clean_and_reshape_eu_klems_variable_type(capital_accounts, national_accounts, growth_accounts, data_info, years_range):
    capital_accounts_clean = clean_eu_klems_data.clean_and_reshape_eu_klems(
        raw=capital_accounts,
        data_info=data_info,
        years=years_range
    )

    national_accounts_clean = clean_eu_klems_data.clean_and_reshape_eu_klems(
        raw=national_accounts,
        data_info=data_info,
        years=years_range
    )

    growth_accounts_clean = clean_eu_klems_data.clean_and_reshape_eu_klems(
        raw=growth_accounts,
        data_info=data_info,
        years=years_range
    )

    capital_accounts_variables = data_info["sheets_to_read"]["intangible_analytical_detailed"][0]
    national_accounts_variables = data_info["sheets_to_read"]["national_accounts"][0]
    growth_accounts_variables = data_info["sheets_to_read"]["growth_accounts"][0]

    assert capital_accounts_clean[capital_accounts_variables].dtypes == np.float64
    assert national_accounts_clean[national_accounts_variables].dtypes == np.float64
    assert growth_accounts_clean[growth_accounts_variables].dtypes == np.float64