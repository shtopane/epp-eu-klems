import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from measuring_intangible_capital.config import SRC
from measuring_intangible_capital.data_management import clean_gdp_data
from measuring_intangible_capital.utilities import read_yaml
from tests.data_management.mock import mock_gdp_data, save_mock_gdp_data, GDP_FIXTURE_PATH

@pytest.fixture(scope="module", autouse=True)
def create_mock_data(request):
    print("Creating mock data")
    gdp = mock_gdp_data()
    save_mock_gdp_data(gdp)

    def remove_mock_data():
        print("Removing mock data")
        os.remove(GDP_FIXTURE_PATH)

    request.addfinalizer(remove_mock_data)

@pytest.fixture()
def data_info():
    """Use real file."""
    return read_yaml(SRC / "data_management" / "gdp_data_info.yaml")

@pytest.fixture()
def gdp_data(data_info):
    gdp = clean_gdp_data.read_data(
        data_info=data_info,
        path=GDP_FIXTURE_PATH
    )

    return gdp

def test_read_data_return_type(data_info):
    gdp = clean_gdp_data.read_data(
        data_info=data_info,
        path=GDP_FIXTURE_PATH
    )

    assert type(gdp) == pd.DataFrame

@pytest.mark.parametrize("data_info", [[], 1, 1.0, True, False, pd.DataFrame()])
def test_read_data_invalid_data_info(data_info):
    with pytest.raises(TypeError, match="The data_info"):
        clean_gdp_data.read_data(
            data_info=data_info,
            path=GDP_FIXTURE_PATH
        )

@pytest.mark.parametrize("path", [[], 1, 1.0, True, False, pd.DataFrame()])
def test_read_data_invalid_path(path, data_info):
    with pytest.raises(ValueError, match="<class 'pathlib.Path'>"):
        clean_gdp_data.read_data(
            data_info=data_info,
            path=path
        )

@pytest.mark.parametrize("raw", [None, 1, 1.0, True, False, "banana", []])
def test_clean_gdp_per_capita_invalid_data(raw, data_info):
    with pytest.raises(BaseException):
        clean_gdp_data.clean_gdp_per_capita(
            raw=raw, 
            data_info=data_info,
        )

def test_clean_gdp_per_capita_return_type(gdp_data, data_info):
    gdp_data_clean = clean_gdp_data.clean_gdp_per_capita(
        raw=gdp_data,
        data_info=data_info
    )

    assert type(gdp_data_clean) == pd.DataFrame

def test_clean_gdp_per_capita_dropna(gdp_data, data_info):
    gdp_data_clean = clean_gdp_data.clean_gdp_per_capita(
        raw=gdp_data,
        data_info=data_info
    )

    assert not gdp_data_clean.isna().any(axis=None)

def test_clean_gdp_per_capita_columns(gdp_data, data_info):
    gdp_data_clean = clean_gdp_data.clean_gdp_per_capita(
        raw=gdp_data,
        data_info=data_info
    )

    assert gdp_data_clean.reset_index().columns.tolist() == ["country_code", "year", "gdp_per_capita"]

def test_clean_gdp_per_capita_gdp_type(gdp_data, data_info):
    gdp_data_clean = clean_gdp_data.clean_gdp_per_capita(
        raw=gdp_data,
        data_info=data_info
    )

    assert gdp_data_clean["gdp_per_capita"].dtype == np.float64

def test_clean_gdp_per_capita_country_code_dtype(gdp_data, data_info):
    gdp_data_clean = clean_gdp_data.clean_gdp_per_capita(
        raw=gdp_data,
        data_info=data_info
    )

    assert gdp_data_clean.reset_index()["country_code"].dtype == "category"