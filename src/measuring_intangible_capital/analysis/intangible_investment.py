"""Functions to calculate intangible investment."""
import numpy as np
import pandas as pd
import math

from measuring_intangible_capital.config import BLD, COUNTRY_CODES, DATA_CLEAN_PATH

import matplotlib.pyplot as plt

def calculate_share_of_intangible_investment(intangible_investment: np.float64, gdp: np.float64) -> np.float64:
    """Calculate intangible investment.

    Args:
        capital_accounts (pandas.DataFrame): Capital accounts data set.
        national_accounts (pandas.DataFrame): National accounts data set.

    Returns:
        pandas.DataFrame: The intangible investment data set.

    """
    return round((intangible_investment / gdp) * 100, 3)

# country_code = "AT"
# capital_accounts: pd.DataFrame = pd.read_pickle(DATA_CLEAN_PATH / country_code / "capital_accounts.pkl")
# national_accounts: pd.DataFrame = pd.read_pickle(DATA_CLEAN_PATH / country_code / "national_accounts.pkl")

def get_gdp_for_year(year: int, country_code: str, df: pd.DataFrame) -> np.float64:
    # return df.loc["TOT", year, country_code].item()
    return df.loc["TOT", year, country_code].item() # df.loc[year, country_code]

def get_intangible_investment_for_year(year: int, country_code: str, df: pd.DataFrame) -> np.float64:
    industry_code = "MARKT"

    # if country_code == "CZ":
    #     industry_code = "MARKTxAG" #"M-N"
    
    return df.loc[industry_code, year, country_code].sum(axis=0)


year_range = range(1995, 2007)
data_for_plotting = pd.DataFrame(columns=["Country", "Investment"])

data = {
    "country_code": [],
    "year": [],
    "intangible_investment": [],
}
# investment_percentages = []

gdp_df = pd.read_pickle(BLD / "python" / "data_clean" / "gdp.pkl")


data_for_plotting_TEST = pd.DataFrame(columns=["country_code", "year", "intangible_investment"])

for country_code in COUNTRY_CODES:
  capital_accounts: pd.DataFrame = pd.read_pickle(DATA_CLEAN_PATH / country_code / "capital_accounts.pkl")
  national_accounts: pd.DataFrame = pd.read_pickle(DATA_CLEAN_PATH / country_code / "national_accounts.pkl")

  for year in year_range:
      intangible_investment = get_intangible_investment_for_year(year, country_code, capital_accounts)
      gdp = get_gdp_for_year(year, country_code, national_accounts)
      share_intangible = calculate_share_of_intangible_investment(intangible_investment, gdp)

      # data_for_plotting_TEST = pd.concat([data_for_plotting_TEST, pd.Series([country_code, year, share_intangible])], axis=0)
      data["country_code"].append(country_code)
      data["year"].append(year)
      data["intangible_investment"].append(calculate_share_of_intangible_investment(intangible_investment, gdp))



print(data)
print(data_for_plotting_TEST)
data_for_plotting = pd.DataFrame(data)
# data_for_plotting.set_index("year", inplace=True)
grouped = data_for_plotting.groupby("country_code")
print(data_for_plotting['intangible_investment'].max())

plt.figure(figsize=(10, 6))
colors = ['gray', 'darkgray', 'lavender', 'lightsteelblue', 'royalblue']
# For each group (i.e., for each country), plot the intangible_investment over the years
for (name, group), color in zip(grouped, colors):
    plt.plot(group['year'], group['intangible_investment'], marker='s', label=name, color=color)

# plt.plot(data_for_plotting, marker="s")
plt.xlabel('Year')
plt.ylabel('Percent of GDP')
plt.title('Intangible Investment for All Countries (1995-2005)')
plt.legend(ncol=len(grouped) , loc='upper center', bbox_to_anchor=(0.5, -0.09))

plt.xticks(year_range)
plt.ylim(1, math.ceil(data_for_plotting['intangible_investment'].max()))

# Show only horizontal grid lines
plt.grid(axis='y')

# Move the x-axis tick lines to the top of the plot
# plt.gca().xaxis.set_tick_params(bottom=True, top=False, labelbottom=True)
plt.subplots_adjust(bottom=0.2)
plt.show()