import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from measuring_intangible_capital.config import TEST_DIR
from measuring_intangible_capital.data_management import clean_eu_klems_data
from measuring_intangible_capital.utilities import read_yaml
from tests.data_management.mock import mock_eu_klems_data

EU_KLEMS_FIXTURE_PATH = TEST_DIR / "data_management" / "eu_klems_data_fixture.xlsx"

@pytest.fixture(scope="module", autouse=True)
def setup_session(request):
    mock_eu_klems_data()
    # def teardown_session():
    #     print("Tearing down the session")
    #     os.remove(EU_KLEMS_FIXTURE_PATH)
    # request.addfinalizer(teardown_session)

@pytest.fixture()
def data():
    return pd.read_excel(EU_KLEMS_FIXTURE_PATH)


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
# def test_clean_data_drop_columns(data, data_info):
#     data_clean = clean_eu_klems_data(data, data_info)
#     assert not set(data_info["columns_to_drop"]).intersection(set(data_clean.columns))


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

# def test_clean_data_dropna(data, data_info):
#     data_clean = clean_eu_klems_data(data, data_info)
#     assert not data_clean.isna().any(axis=None)


# def test_clean_data_categorical_columns(data, data_info):
#     data_clean = clean_eu_klems_data(data, data_info)
#     for cat_col in data_info["categorical_columns"]:
#         renamed_col = data_info["column_rename_mapping"].get(cat_col, cat_col)
#         assert data_clean[renamed_col].dtype == "category"


# def test_clean_data_column_rename(data, data_info):
#     data_clean = clean_eu_klems_data(data, data_info)
#     old_names = set(data_info["column_rename_mapping"].keys())
#     new_names = set(data_info["column_rename_mapping"].values())
#     assert not old_names.intersection(set(data_clean.columns))
#     assert new_names.intersection(set(data_clean.columns)) == new_names


# def test_convert_outcome_to_numerical(data, data_info):
#     data_clean = clean_eu_klems_data(data, data_info)
#     outcome_name = data_info["outcome"]
#     outcome_numerical_name = data_info["outcome_numerical"]
#     assert outcome_numerical_name in data_clean.columns
#     assert data_clean[outcome_name].dtype == "category"
#     assert data_clean[outcome_numerical_name].dtype == np.int8
