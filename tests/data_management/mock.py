"""Functions to mock data sets for testing purposes."""
import pandas as pd

from measuring_intangible_capital.config import TEST_DIR


def mock_eu_klems_data():
    """Mock the EU KLEMS data set.
    The data set is a multi-sheet Excel where each variable of interest(say intangible investment) is in a separate sheet.
    In each sheet the variables are: nace_r2_code, geo_code, geo_name, nace_r2_name and then for each year the var values.
    """
    capital_accounts = pd.DataFrame(
        {
            **_get_base_data(),
            "var": ["Capital_Variable", "Capital_Variable", "Capital_Variable"],
        }
    )

    national_accounts = pd.DataFrame(
        {
            **_get_base_data(),
            "var": ["National_Variable", "National_Variable", "National_Variable"],
        }
    )

    growth_accounts = pd.DataFrame(
        {
            **_get_base_data(),
            "var": ["Growth_Variable", "Growth_Variable", "Growth_Variable"],
        }
    )

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(
        TEST_DIR / "data_management" / "eu_klems_data_fixture.xlsx", engine="xlsxwriter"
    ) as writer:
        capital_accounts.to_excel(writer, sheet_name="Capital_Variable", index=False)
        national_accounts.to_excel(writer, sheet_name="National_Variable", index=False)
        growth_accounts.to_excel(writer, sheet_name="Growth_Variable", index=False)


def _get_base_data():
    """Get the base data for the mock."""
    base_data = {
        "nace_r2_code": ["A", "B", "C"],
        "1995": [1, 2, 3],
        "1996": [4, 5, 6],
        "1997": [7, 8, 9],
        "geo_code": ["AT", "AT", "AT"],
        "geo_name": ["Austria", "Austria", "Austria"],
        "nace_r2_name": ["Agriculture", "Mining", "Manufacturing"]
    }
    return base_data
