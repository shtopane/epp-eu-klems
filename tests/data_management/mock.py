import pandas as pd

from measuring_intangible_capital.config import TEST_DIR


def mock_eu_klems_data():
    """Mock the EU KLEMS data set.
    3 columns are must haves: industry_code, year, country_code.
    Then, others can be added.
    """
    capital_accounts = pd.DataFrame(
        {
            **_get_base_data(),
            "var": ["Sheet1", "Sheet1", "Sheet1"],
        }
    )

    national_accounts = pd.DataFrame(
        {
            **_get_base_data(),
            "var": ["Sheet2", "Sheet2", "Sheet2"],
        }
    )

    growth_accounts = pd.DataFrame(
        {
            **_get_base_data(),
            "var": ["Sheet3", "Sheet3", "Sheet3"],
        }
    )

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(
        TEST_DIR / "data_management" / "eu_klems_data_fixture.xlsx", engine="xlsxwriter"
    ) as writer:
        capital_accounts.to_excel(writer, sheet_name="Sheet1", index=False)
        national_accounts.to_excel(writer, sheet_name="Sheet2", index=False)
        growth_accounts.to_excel(writer, sheet_name="Sheet3", index=False)


def _get_base_data():
    """Get the base data for the mock."""
    base_data = {
        "nace_r2_code": ["A", "B", "C"],
        "1995": [1, 2, 3],
        "1996": [4, 5, 6],
        "1997": [7, 8, 9],
        "geo_code": ["AT", "AT", "AT"],
    }
    return base_data
