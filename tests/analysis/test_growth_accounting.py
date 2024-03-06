# Invoke function and check that the output is correct
# # TEST(check that labour compensation + capital compensation = gdp for each year)
# labour_compensation_2006 = growth_accounting_SK.loc["TOT", 2006, :]["labour_compensation"]
# capital_compensation_2006 = growth_accounting_SK.loc["TOT", 2006, :]["capital_compensation"]
# gdp_2006 = national_accounts_SK.loc["TOT", 2006, :]["gdp"]
# print(labour_compensation_2006 + capital_compensation_2006 == gdp_2006)