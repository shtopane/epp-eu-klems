import pandas as pd

from measuring_intangible_capital.config import DATA_CLEAN_PATH

def _calculate_labour_compensation(national_accounts: pd.DataFrame) -> pd.Series:
    # LAB_j = COMP_j + (COMP_j / HEMPE_j) * (HEMP_j - HEMPE_j)
    return national_accounts["compensation_of_employees"] + (
        national_accounts["compensation_of_employees"]
        / national_accounts["hours_worked_persons"]
    ) * (
        national_accounts["hours_worked_persons"]
        - national_accounts["hours_worked_employees"]
    )

def _calculate_capital_compensation(national_accounts: pd.DataFrame, growth_accounts: pd.DataFrame) -> pd.Series:
    # CAP(capital compensation) = gdp - labour_compensation
    df = growth_accounts.copy()

    df["capital_compensation"] = national_accounts["gdp"] - growth_accounts["labour_compensation"]
    
    # page 18, EU KLEMS manual Deliverable D2.3.1 February 2023
    # Replace negative capital accumulation with 95% of the GDP and labour compensation for the same
    # records with 5% of GDP
    negative_capital_accumulation = df["capital_compensation"] < 0
    df.loc[negative_capital_accumulation, "capital_compensation"] = (
        0.95 * national_accounts["gdp"]
    )
    df.loc[negative_capital_accumulation, "labour_compensation"] = (
        0.05 * national_accounts["gdp"]
    )

    return df

def main(national_accounts: pd.DataFrame):
    # Start with empty DataFrame
    df = pd.DataFrame()

    # FIRST
    df["labour_compensation"] = _calculate_labour_compensation(national_accounts)

    # SECOND
    df = _calculate_capital_compensation(national_accounts, df)

    return df

national_accounts_SK = pd.read_pickle(DATA_CLEAN_PATH / "SK" / "national_accounts.pkl")

print(national_accounts_SK["gdp"])

growth_accounting_SK = main(national_accounts_SK)
print(growth_accounting_SK.loc["TOT", 2006, :]["capital_compensation"])
print(growth_accounting_SK.loc["TOT", 2006, :]["labour_compensation"])

# TEST(check that labour compensation + capital compensation = gdp for each year)
labour_compensation_2006 = growth_accounting_SK.loc["TOT", 2006, :]["labour_compensation"]
capital_compensation_2006 = growth_accounting_SK.loc["TOT", 2006, :]["capital_compensation"]
gdp_2006 = national_accounts_SK.loc["TOT", 2006, :]["gdp"]
print(labour_compensation_2006 + capital_compensation_2006 == gdp_2006)